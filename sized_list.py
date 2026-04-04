from functions.myrange import geometry_prog

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
    def __init__(self, state = []):
        self.state = sorted(state)
        self.n = len(state)

    def add(self, value):
        for i in range(self.n):
            if value < self.state[i]:
                self.state.insert(i, value)
                return
        self.state.append(value)
        

    def __repr__(self):
        return f"sorted_list({self.state})"


a = sorted_list([1,2,3])
print(a.state)
for i in geometry_prog(2, 10000, -2):
    a.add(i)
    print(a)