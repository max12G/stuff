from functions.myrange import geometry_prog
from functions.funcs_help import binsearch

class sized_list:
    def __init__(self, size = 0, state = []):
        self.state = state + [None] * (size - len(state))
        self.size = size
        self.current = len(state)
        self.full = size == len(state)

    def add(self, value):
        if self.current >= self.size:
            self.current = 0
            self.full = True
        self.state[self.current] = value
        self.current += 1

    def __iter__(self):
        i = self.current
        if not self.full:
            return iter(self.state[:i])
        return iter(self.state[i:] + self.state[:i])

    def clear(self):
        self.state = [None] * self.size

    def __repr__(self):
        return f"sized_list({list(self)})"

    def __len__(self):
        return self.size if self.full else self.current


class sorted_list:
    def __init__(self, state = [], ascendic = True):
        self.state = sorted(state, reverse=not(ascendic))
        self.n = len(state)
        self.ascendic = ascendic
        self.total_sum = sum(self.state)
        self.size = len(self.state)

    def add(self, value):
        if not self.state:
            self.size += 1
            self.total_sum += value
            self.state.append(value)
            return
        if value > self.state[-1]:
            self.size += 1
            self.total_sum += value
            if self.ascendic:
                self.state.append(value)
                return
            self.state.insert(0, value)
            return
        if value < self.state[0]:
            self.size += 1
            self.total_sum += value
            if self.ascendic:
                self.state.insert(0, value)
                return
            self.state.append(value)
            return
        index = binsearch(value, self.state)
        self.state.insert(index, value)
        self.total_sum += value
        self.size += 1
        return

    def max(self):
        if not self.state:
            return
        if self.ascendic:
            return self.state[-1]
        return self.state[0]
        
    def min(self):
        if not self.state:
            return
        if self.ascendic:
            return self.state[0]
        return self.state[-1]
    
    def mean(self):
        return self.total_sum / self.size
    
    def median(self):
        if self.size % 2 == 0:
            return (self.state[self.size // 2] + self.state[self.size // 2 - 1]) / 2
        return self.state[self.size // 2]
    
    def variance(self):
        mn = self.mean()
        s = 0
        for val in self.state:
            s += (mn - val) ** 2
        return s / self.size
    
    def merge(self, other):
        if self.ascendic != other.ascendic:
            raise TypeError("Both lists need same type sorting")
        result = sorted_list([], ascendic=self.ascendic)
        result.total_sum = self.total_sum + other.total_sum
        result.size = self.size + other.size
        n1, n2 = 0, 0
        while n1 < self.size and n2 < other.size:
            if self.ascendic:
                choose_first = self.state[n1] <= other.state[n2]
            else:
                choose_first = self.state[n1] >= other.state[n2]
            if choose_first:
                result.state.append(self.state[n1])
                n1 += 1
            else:
                result.state.append(other.state[n2])
                n2 += 1
        if n1 < self.size:
            result.state.extend(self.state[n1:])
        if n2 < other.size:
            result.state.extend(other.state[n2:])
        return result

    def remove(self, value):
        index = binsearch(value, self.state)
        if index < len(self.state) and self.state[index] == value:
            del self.state[index]
            self.size -= 1
            self.total_sum -= value
            return
        raise ValueError(f"{value} not in sorted_list")
    
    def quantile(self, q):
        if not 0 <= q <= 1:
            raise ValueError("quantile must be between 0 and 1")
        index = int(q * (self.size  - 1))
        return self.state[:index]
    
    def find_pop(self):
        if not self.state:
            return 
        pop_val = self.state[0]
        curr = 1
        max_seq = 1
        for i in range(1, self.size):
            if self.state[i] == self.state[i - 1]:
                curr += 1
            else:
                if curr > max_seq:
                    pop_val = self.state[i - 1]
                    max_seq = curr
        if curr > max_seq:
            pop_val = self.state[-1]
        return pop_val
                
    def __repr__(self):
        return f"sorted_list({self.state})"
