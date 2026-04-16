from time import perf_counter, sleep


def binsearch(target, source):
    left = 0
    right = len(source) - 1
    while left <= right:
        middle = (left + right) // 2
        if target > source[middle]:
            left = middle + 1
        elif target == source[middle]:
            return middle
        else:
            right = middle - 1
    return left


def safe_wraps(func: callable) -> callable:
    def decorator(wrapper: callable) -> callable:
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__annotations__ = func.__annotations__
        wrapper.__wrapped__ = func
        return wrapper
    return decorator


def timer(func: callable) -> callable:
    @safe_wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        res = func(*args, **kwargs)
        print(f"Total complition time: {perf_counter() - start:.2f} sec.")
        return res
    return wrapper


def safe_launch(func: callable) -> callable:
    @safe_wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            print(f"Function has interrupted by {e}")
            return None
    return wrapper


class func_cache:
    def __init__(self, func: callable):
        self.storage = {}
        self.wrap_func = self._setup(func)
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
        self.__annotations__ = getattr(func, "__annotations__", {})
        self.__wrapped__ = func

    def _setup(self, func):
        @safe_wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in self.storage:
                self.storage[key] = func(*args, **kwargs)
            return self.storage[key]
        return wrapper

    def __call__(self, *args, **kwargs):
        return self.wrap_func(*args, **kwargs)
    
    def clear(self):
        self.storage.clear()


class time_limiter:
    def __init__(self, rate: float = 1):
        self.rate = rate
        self.last_using = perf_counter()

    def __call__(self, func):
        @safe_wraps(func)
        def wrapper(*args, **kwargs):
            curr = perf_counter()
            self.last_using = curr
            if curr - self.last_using < self.rate:
                sleep(self.rate - curr + self.last_using)
                self.last_using = curr
            return func(*args, **kwargs)
        return wrapper


class rate_limiter:
    def __init__(self, calls: int = 1, period: float = 1):
        self.calls = calls
        self.period = period
        self.tokens = calls
        self.last_call = perf_counter()
    
    def __call__(self, func):
        @safe_wraps(func)
        def wrapper(*args, **kwargs):
            curr = perf_counter()
            passed = curr - self.last_call
            self.tokens += passed * (self.calls / self.period)
            if self.tokens > self.calls:
                self.tokens = self.calls

            self.last_call = curr

            if self.tokens < 1:
                wait_time = (1 - self.tokens) * (self.period / self.calls)
                sleep(wait_time)
                self.last_call = perf_counter()
                self.tokens = 1
            self.tokens -= 1

            return func(*args, **kwargs)
        return wrapper
        

def retry(count_tries: int = 3, delay: float = 0.5) -> callable:
    def decorator(func: callable):
        @safe_wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, count_tries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt}/{count_tries} failed: {e}")
                    if attempt < count_tries:
                        sleep(delay)
            print(f"All {count_tries} attempts failed.")
            return None
        return wrapper
    return decorator


def type_checker(func: callable):
    def wrapper(*args, **kwargs):
        annot = func.__annotations__
        names = func.__code__.co_varnames[:func.__code__.co_argcount]

        for arg, val in zip(names, args):
            need = annot.get(arg, None)
            if need is None:
                continue
            if not isinstance(val, need):
                raise TypeError(f"Argument '{arg}' must be {need}, not {type(val)}")

        for arg, val in kwargs.items():
            need = annot.get(arg, None)
            if need is None:
                continue
            if not isinstance(val, need):
                raise TypeError(f"Argument '{arg}' must be {need}, not {type(val)}")
        return func(*args, **kwargs)
    return wrapper


def circuit_breaker(max_fails: int = 5, recovery_timeout: float = 0.5):
    fails = 0
    last_exception = None
    last_fail_time = 0
    def decorator(func: callable):
        @safe_wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal fails, last_exception, last_fail_time
            now = perf_counter()
            if fails >= max_fails:
                if now - last_fail_time < recovery_timeout:
                    print(f"System is broken. Remaining: {recovery_timeout - (now - last_fail_time):.1f}sec.")
                    raise last_exception
                else:
                    print("Half-Open: testing the connection...")
            try:
                res = func(*args, **kwargs)
                fails = 1
                return res  
            except Exception as e:
                fails += 1
                last_exception = e
                raise e
        return wrapper
    return decorator

            


import time

# --- Тест 1: Кэширование (func_cache) ---
@timer
@func_cache
def heavy_computation(n):
    # Имитируем тяжелые вычисления
    time.sleep(1)
    return n * 2

# --- Тест 2: Ограничение частоты (rate_limiter) ---
# Ограничим: не более 2 вызовов в секунду
@rate_limiter(calls=2, period=1)
def api_request(i):
    return f"Request {i} done"

# --- Тест 3: Предохранитель (circuit_breaker) ---
@circuit_breaker(max_fails=3, recovery_timeout=2)
def unstable_service():
    print("  [Service] Trying to work...")
    raise ConnectionError("Server is down")

# --- Запуск испытаний ---

def run_performance_suite():
    print("=== ИСПЫТАНИЕ 1: Кэширование ===")
    print("Первый вызов (должен быть 1с):")
    heavy_computation(10)
    print("Повторный вызов (должен быть мгновенным):")
    heavy_computation(10)
    
    print("\n=== ИСПЫТАНИЕ 2: Rate Limiter (2 вызова/сек) ===")
    start = time.perf_counter()
    for i in range(4):
        print(f"  {api_request(i)} at {time.perf_counter() - start:.2f}s")

    print("\n=== ИСПЫТАНИЕ 3: Circuit Breaker ===")
    for i in range(5):
        try:
            print(f"Попытка {i+1}:")
            unstable_service()
        except Exception:
            pass
        time.sleep(0.1)
    
    print("\nОжидаем таймаут восстановления (2 сек)...")
    time.sleep(2)
    try:
        print("Попытка после паузы (Half-Open):")
        unstable_service()
    except Exception:
        print("Система все еще нестабильна, цепь снова разомкнута.")

if __name__ == "__main__":
    run_performance_suite()