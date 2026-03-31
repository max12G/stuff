import sys
import numpy as np
import pandas as pd
from collections import deque
from time import perf_counter
import tracemalloc
import math



class myrange:
    __slots__ = 'start', 'end', 'step', 'flag_to_str'
    def __init__(self, *args):
        self.step = 1
        self.start = 0
        self.flag_to_str = False
        n = len(args)
        if n == 1:
            self.end = args[0]
        elif n == 2:
            self.start, self.end = args[0], args[1]
        elif n == 3:
            self.start, self.end, self.step = args
        else:
            raise TypeError(f"Excepted at most 3 arguments, got {n}")

        if self.step == 0:
            raise ValueError("myrange() step must not be zero")
        
        if isinstance(self.start, str):
            if isinstance(self.end, str):
                try:
                    self.start = ord(self.start)
                    self.end = ord(self.end)
                    self.flag_to_str = True
                except TypeError:
                    raise TypeError("Both elements must be 1 symbols")
            else:
                raise ValueError("Need both string-type objects")


    def __iter__(self):
        curr = self.start
        if self.step > 0:
            i = 1
            while curr < self.end:
                if self.flag_to_str:
                    yield chr(curr)
                else:
                    yield round(curr, 5)
                curr = self.start + self.step * i
                i += 1
        elif self.step < 0:
            i = 1
            while curr > self.end:
                if self.flag_to_str:
                    yield chr(curr)
                else:
                    yield round(curr, 5)
                curr = self.start + self.step * i
                i += 1

    def __contains__(self, item):
        if self.flag_to_str and isinstance(item, str) and len(item) == 1:
            item = ord(item)
        if self.flag_to_str == 0 and isinstance(item, str):
            return False
        if self.step < 0 and (item > self.start or item < self.end):
            return False
        if self.step > 0 and (item < self.start or item > self.end):
            return False
        if item == self.end:
            return False
        eps = 1e-10
        steps = (item - self.start) / self.step
        return abs(steps - round(steps)) < eps
    
    def __len__(self):
        if self.step > 0 and self.start < self.end:
            return (self.end - self.start - 1) // self.step + 1
        elif self.step < 0 and self.start > self.end:
            return (self.start - self.end - 1) // (-self.step) + 1
        return 0
    
    def __getitem__(self, key):
        size = len(self)
        if isinstance(key, int):
            if self.flag_to_str:
                if key < 0: key += size
                if key < 0 or key >= size: raise IndexError("index out of range")
                return chr(self.start + (self.step * key))
            
            if key < 0: key += size
            if key < 0 or key >= size: raise IndexError("index out of range")
            return self.start + (self.step * key)

        if isinstance(key, slice):
            start, end, step = key.indices(len(self))
            new_start = self.__getitem__(start)
            if self.flag_to_str:
                new_start = ord(new_start)
            new_step = self.step * step
            new_len = max(0, (end - start + step - (1 if step > 0 else -1)) // step)
            new_end = new_start + new_len * new_step
            if self.flag_to_str:
                return myrange(chr(new_start), chr(new_end), new_step)
            return myrange(new_start, new_end, new_step)
        
    def __repr__(self):
        if self.flag_to_str:
            return f"Object myrange: start > {chr(self.start)}, stop > {chr(self.end)}, step > {self.step}"
        return f"Object myrange: start > {self.start}, stop > {self.end}, step > {self.step}"

    def __reversed__(self):
        if len(self) == 0:
            return self
        start = self[-1]
        step = self.step * -1
        end = self.start + step
        return myrange(start, end, step)
    
    def __eq__(self, other):
        if not isinstance(other, myrange):
            return NotImplemented
        size = len(self)
        if size != len(other):
            return False
        if size == 0:
            return True
        return self.start == other.start and self.step == other.step
    
    def __hash__(self):
        if len(self) == 0:
            return hash((0, None, None))
        return hash((len(self), self.start, self.step))
    
    def index(self, value):
        if value in self:
            return (value - self.start) // self.step
        raise ValueError(f"{value} not in myrange")
    
    def sum(self):
        n = len(self)
        last = self[-1]
        if self.flag_to_str:
            last = ord(last)
        return (self.start + last) / 2 * n
    
    def mean(self):
        last = self[-1]
        if self.flag_to_str:
            last = ord(last)
        return (self.start + last) / 2
    
    def max(self):
        if self.flag_to_str:
            if self.step > 0:
                return chr(self[-1])
            else:
                return chr(self.start)
        if self.step > 0:
            return self[-1]
        else:
            return self.start
        
    def min(self):
        if self.flag_to_str:
            if self.step < 0:
                return chr(self[-1])
            else:
                return chr(self.start)
        if self.step < 0:
            return self[-1]
        else:
            return self.start
        
    def info(self):
        print(f" id -> {id(self)}")
        print(f" type -> {"string" if self.flag_to_str else "number"}")
        print(f" max -> {max(self)}")
        print(f" min -> {min(self)}")
        print(f" mean -> {self.mean()}")
        print(f" sum -> {self.sum()}")
        print(f" size -> {len(self)}")





class arifm_prog:
    __slots__ = 'start', 'end', 'step'
    def __init__(self, *args):
        self.step = 1
        self.start = 0
        n = len(args)
        if n == 1:
            self.end = args[0]
        elif n == 2:
            self.start, self.end = args[0], args[1]
        elif n == 3:
            self.start, self.end, self.step = args
        else:
            raise TypeError(f"Excepted at most 3 arguments, got {n}")

        if self.step == 0:
            raise ValueError("arifm_prog() step must not be zero")

    def __iter__(self):
        curr = self.start
        if self.step > 0:
            i = 1
            while curr < self.end:
                yield round(curr, 5)
                curr = self.start + self.step * i
                i += 1
        elif self.step < 0:
            i = 1
            while curr > self.end:
                yield round(curr, 5)
                curr = self.start + self.step * i
                i += 1

    def __contains__(self, item):
        if self.step < 0 and (item > self.start or item < self.end):
            return False
        if self.step > 0 and (item < self.start or item > self.end):
            return False
        if item == self.end:
            return False
        eps = 1e-10
        steps = (item - self.start) / self.step
        return abs(steps - round(steps)) < eps
    
    def __len__(self):
        if self.step > 0 and self.start < self.end:
            return (self.end - self.start - 1) // self.step + 1
        elif self.step < 0 and self.start > self.end:
            return (self.start - self.end - 1) // (-self.step) + 1
        return 0
    
    def __getitem__(self, key):
        size = len(self)
        if isinstance(key, int):
            
            if key < 0: key += size
            if key < 0 or key >= size: raise IndexError("index out of range")
            return self.start + (self.step * key)

        if isinstance(key, slice):
            start, end, step = key.indices(len(self))
            new_start = self.__getitem__(start)
            new_step = self.step * step
            new_len = max(0, (end - start + step - (1 if step > 0 else -1)) // step)
            new_end = new_start + new_len * new_step
            if self.flag_to_str:
                return arifm_prog(chr(new_start), chr(new_end), new_step)
            return arifm_prog(new_start, new_end, new_step)
        
    def __repr__(self):
        return f"Object arifm_prog: start > {self.start}, stop > {self.end}, step > {self.step}"

    def __reversed__(self):
        if len(self) == 0:
            return self
        start = self[-1]
        step = self.step * -1
        end = self.start + step
        return arifm_prog(start, end, step)
    
    def __eq__(self, other):
        if not isinstance(other, arifm_prog):
            return NotImplemented
        size = len(self)
        if size != len(other):
            return False
        if size == 0:
            return True
        return self.start == other.start and self.step == other.step
    
    def __hash__(self):
        if len(self) == 0:
            return hash((0, None, None))
        return hash((len(self), self.start, self.step))
    
    def index(self, value):
        if value in self:
            return (value - self.start) // self.step
        raise ValueError(f"{value} not in arifm_prog")
    
    def sum(self):
        n = len(self)
        last = self[-1]
        return (self.start + last) / 2 * n
    
    def mean(self):
        last = self[-1]
        return (self.start + last) / 2
    
    def max(self):
        if self.step > 0:
            return self[-1]
        else:
            return self.start
        
    def min(self):
        if self.step < 0:
            return self[-1]
        else:
            return self.start
        
    def info(self):
        print(f" id -> {id(self)}")
        print(f" max -> {max(self)}")
        print(f" min -> {min(self)}")
        print(f" mean -> {self.mean()}")
        print(f" sum -> {self.sum()}")
        print(f" size -> {len(self)}")





class geometry_prog:
    __slots__ = 'start', 'end', 'step'
    def __init__(self, *args):
        self.step = 1
        self.start = 0
        n = len(args)
        if n == 1:
            self.end = args[0]
        elif n == 2:
            self.start, self.end = args[0], args[1]
        elif n == 3:
            self.start, self.end, self.step = args
        else:
            raise TypeError(f"Excepted at most 3 arguments, got {n}")

        if self.step == 0 or self.step == 1:
            raise ValueError("geometry_prog() step must not be zero or one")

    def __iter__(self):
        curr = self.start
        while curr < self.end:
            yield round(curr, 5)
            curr *= self.step

    def __contains__(self, item):
        if item > self.end:
            return False
        if self.step > 0 and item * self.start < 0:
            return False
        res = math.log(abs(item / self.start), abs(self.step))
        return self.start * self.step ** res == item
    
    def __len__(self):
        res = math.log(abs(self.end / self.start), abs(self.step))
        if res < 0:
            return 0
        return math.ceil(res)

    def __getitem__(self, key):
        size = len(self)
        if isinstance(key, int):
            if key < 0: key += size
            if key < 0 or key >= size: raise IndexError("index out of range")
            return self.start * self.step ** key

        if isinstance(key, slice):
            start, end, step = key.indices(len(self))
            new_start = self.__getitem__(start)
            new_step = self.step ** step
            end_ = self[end]
            new_len = int(math.log(end_ / new_start, new_step))
            new_end = new_start * new_step ** new_len
            return geometry_prog(new_start, new_end, new_step)
        
    def __repr__(self):
        return f"Object geometry_prog: start > {self.start}, stop > {self.end}, step > {self.step}"

    def __reversed__(self):
        if len(self) == 0:
            return self
        start = self[-1]
        step = 1 / self.step
        end = self.start + step
        return geometry_prog(start, end, step)
    
    def __eq__(self, other):
        if not isinstance(other, geometry_prog):
            return NotImplemented
        size = len(self)
        if size != len(other):
            return False
        if size == 0:
            return True
        return self.start == other.start and self.step == other.step
    
    def __hash__(self):
        if len(self) == 0:
            return hash((0, None, None))
        return hash((len(self), self.start, self.step))
    
    def index(self, value):
        if value in self:
            return math.log(value / self.start, self.step)
        raise ValueError(f"{value} not in geometry_prog")
    
    def sum(self):
        n = len(self)
        return (self.start * (1 - self.step ** n) / (1 - self.step))
    
    def mean(self):
        n = len(self)
        return self.sum() / n
    
    def max(self):
        if len(self) == 0:
            return None
        if abs(self.step) > 1:
            if self.step < 0:
                return max(self[-1], self[-2])
            return self[-1]
        else:
            if self.step < 0:
                return max(self.start, self[1])
            return self.start
        
    def min(self):
        if len(self) == 0:
            return None
        if abs(self.step) < 1:
            if self.step < 0:
                return min(self[-1], self[-2])
            return self[-1]
        else:
            if self.step < 0:
                return max(self.start, self[1])
            return self.start
        
    def info(self):
        print(f" id -> {id(self)}")
        print(f" max -> {max(self)}")
        print(f" min -> {min(self)}")
        print(f" mean -> {self.mean()}")
        print(f" sum -> {self.sum()}")
        print(f" size -> {len(self)}")


