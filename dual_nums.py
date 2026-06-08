import math
from typing import Callable

class Dual_Number:
    def __init__(self, base: int | float, dual: int| float):
        self.base = base
        self.dual = dual

    def __add__(self, other: float | int | Dual_Number) -> Dual_Number:
        base = 0
        dual = 0
        if isinstance(other, (int, float)):
            base = self.base + other
            dual = self.dual
        else:
            base = self.base + other.base
            dual = self.dual + other.dual
        return Dual_Number(base=base, dual=dual)
    
    def __radd__(self, other: float | int) -> Dual_Number:
        return self + other
    
    def __mul__(self, other: float | int | Dual_Number) -> Dual_Number:
        base = 0
        dual = 0
        if isinstance(other, (int, float)):
            base = self.base * other
            dual = self.dual * other
        else:
            base = self.base * other.base
            dual = other.dual * self.base + self.dual * other.base
        return Dual_Number(base=base, dual=dual)

    def __rmul__(self, other: float | int | Dual_Number) -> Dual_Number:
        return self * other
    
    def __truediv__(self, other: float | int | Dual_Number) -> Dual_Number:
        base = 0
        dual = 0
        if isinstance(other, (int, float)):
            base = self.base / other
            dual = self.dual / other
        else:
            base = self.base / other.base
            dual = (self.dual * other.base - self.base * other.dual) / other.base ** 2
        return Dual_Number(base=base, dual=dual)
    
    def __rtruediv__(self, other: float | int) -> Dual_Number:
        base = 0
        dual = 0
        if self.base == 0:
            raise ZeroDivisionError("Деление невозможно: вещественная часть знаменателя равна нулю.")
        else:
            base = other / self.base
            dual = -other * self.dual / (self.base ** 2)
        return Dual_Number(base=base, dual=dual)
    
    def __pow__(self, other: int) -> Dual_Number:
        base = self.base ** other
        dual = self.dual * self.base ** (other - 1) * other
        return Dual_Number(base=base, dual=dual)
    
    def __sub__(self, other: float | int | Dual_Number) -> Dual_Number:
        base = 0
        dual = 0
        if isinstance(other, (int, float)):
            base = self.base - other
            dual = self.dual
        else:
            base = self.base - other.base
            dual = self.dual - other.dual
        return Dual_Number(base=base, dual=dual)
        
    def __rsub__(self, other: float | int | Dual_Number) -> Dual_Number:
        base = 0
        dual = 0
        if isinstance(other, (int, float)):
            base = other - self.base
            dual = -self.dual
        else:
            base = other.base - self.base
            dual = other.dual - self.dual
        return Dual_Number(base=base, dual=dual)

def sin(z: Dual_Number | float | int) -> Dual_Number | float:
    if isinstance(z, (int, float)):
        return math.sin(z)
    return Dual_Number(math.sin(z.base), math.cos(z.base) * z.dual)
    
def cos(z: Dual_Number | float | int) -> Dual_Number | float:
    if isinstance(z, (int, float)):
        return math.cos(z)
    return Dual_Number(math.cos(z.base), -math.sin(z.base) * z.dual)


class Auto_Differ:
    def __init__(self):
        pass

    def find_gradient(self, function: Callable[[Dual_Number], Dual_Number], scalar: float | int) -> float | int:
        x = Dual_Number(scalar, 1)
        result = function(x)
        return result.dual


def run_ultra_stress_test(differ: Auto_Differ):
    print("=== ЗАПУСК УЛЬТРА-СТРЕСС-ТЕСТА ===\n")

    # ----------------------------------------------------------------
    # ТЕСТ 1: Множественное ветвление переменной (Башня плотности)
    # Функция: f(x) = x * x * x * x * x - x^2 (расписано вручную без больших степеней)
    # f(x) = (((x * x) * x) * x) - (x * x)
    # Производная: f'(x) = 5x^4 - 2x
    # В точке x = 2: f'(2) = 5(16) - 4 = 80 - 4 = 76
    # Тест проверяет, корректно ли работает накопление Im-части при умножении Dual * Dual
    # ----------------------------------------------------------------
    try:
        res1 = differ.find_gradient(lambda x: (((x * x) * x) * x) - (x * x), 2)
        assert math.isclose(res1, 76), f"Ожидалось 76, получено {res1}"
        print("Тест 1 (Умножение дуального на дуальное многократно): УСПЕШНО")
    except Exception as e:
        print(f"Тест 1 (Башня плотности): СБОЙ -> {e}")

    # ----------------------------------------------------------------
    # ТЕСТ 2: Глубокая вложенность дробей (Цепная дробь)
    # Функция: f(x) = 1 / (x + 1 / (x + 1 / x))
    # В точке x = 1. Нам нужно аналитически посчитать производную.
    # Облегчим проверку: Python сделает это сам через дуальные числа, 
    # а мы сравним с точным эталоном, вычисленным вручную: f'(1) = -0.2
    # Тест беспощадно проверяет __rtruediv__ и __add__ в цикле.
    # ----------------------------------------------------------------
    try:
        res2 = differ.find_gradient(lambda x: 1 / (x + 1 / (x + 1 / x)), 1)
        assert math.isclose(res2, -0.2), f"Ожидалось -0.2, получено {res2}"
        print("Тест 2 (Вложенная цепная дробь): УСПЕШНО")
    except Exception as e:
        print(f"Тест 2 (Цепная дробь): СБОЙ -> {e}")

    # ----------------------------------------------------------------
    # ТЕСТ 3: Аппроксимация экспоненты (Закон Эйлера)
    # Функция: f(x) = (1 + x / n) ^ n  (при большом n это e^x)
    # Возьмем n = 10000. При x = 1, f(1) ≈ e ≈ 2.71828...
    # Производная e^x равна e^x. То есть f'(1) должна быть очень близка к f(1).
    # ----------------------------------------------------------------
    try:
        n = 10000
        res3 = differ.find_gradient(lambda x: (1 + x / n) ** n, 1)
        expected = (1 + 1 / n) ** (n - 1) # аналитическая производная этой функции в x=1
        assert math.isclose(res3, expected, rel_tol=1e-9), f"Ожидалось {expected}, получено {res3}"
        print("Тест 3 (Предел Эйлера / Аппроксимация e^x): УСПЕШНО")
    except Exception as e:
        print(f"Тест 3 (Предел Эйлера): СБОЙ -> {e}")

    # ----------------------------------------------------------------
    # ТЕСТ 4: Отрицательные и дробные значения вещественной части
    # Функция: f(x) = x^3 - 2/x
    # Производная: f'(x) = 3x^2 + 2/x^2
    # В отрицательной точке x = -0.5:
    # f'(-0.5) = 3*(-0.5)^2 + 2/(-0.5)^2 = 3*(0.25) + 2/(0.25) = 0.75 + 8 = 8.75
    # ----------------------------------------------------------------
    try:
        res4 = differ.find_gradient(lambda x: (x ** 3) - 2 / x, -0.5)
        assert math.isclose(res4, 8.75), f"Ожидалось 8.75, получено {res4}"
        print("Тест 4 (Отрицательный дробный аргумент): УСПЕШНО")
    except Exception as e:
        print(f"Тест 4 (Отрицательный аргумент): СБОЙ -> {e}")

    print("\n=== УЛЬТРА-ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")

diff = Auto_Differ()
run_ultra_stress_test(diff)