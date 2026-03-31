



class myset:
    def __init__(self, elements: list = []):
        self.elements = self.prepare_list(elements)
        self.min = sorted(self.elements)
        self.max = sorted(self.elements, reverse=True)
        self.sum = sum(self.elements)

    def __contains__(self, item):
        for el in self.elements:
            if el == item:
                return True
        return False

    def __getitem__(self, key):
        n = len(self.elements)
        if isinstance(key, int):
            if key < 0:
                key = n - key
            if key >= n:
                raise IndexError("myset() index out of range")
        if isinstance(key, slice):
            return myset(self.elements[key])
    
        
    def __repr__(self):
        return "{" + ", ".join(map(str, self.elements)) + "}"

    def add(self, item) -> None:
        if item not in self.elements:
            self.elements.append(item)
            if not self.max:
                self.max.append(item) 
                self.min.append(item)
                return
            if item > self.max[0]:
                self.max.append(item)
            if item < self.min[0]:
                self.min.append(item)
        return

    def pop(self, index):
        n = len(self.elements)
        if index < 0:
            index = n + index
        if index >= n:
            raise IndexError("myset() index out of range")
        result = self.elements.pop(index)
        if result in self.min:
            self.min.remove(result)
        if result in self.max:
            self.max.remove(result)                             
        return result
    
    def get_min(self):
        return self.min[-1]
    
    def get_max(self):
        return self.max[-1]

    def prepare_list(self, elements: list = []):
        n = len(elements)
        i = 0
        while i < n - 1:
            if elements[i] == elements[i + 1]:
                del elements[i]
                n -= 1
                i -= 1
            i += 1
        return elements
    
    def unity(self, other):
        new_elements = []
        for i in self.elements:
            if i in other.elements:
                new_elements.append(i)
        return myset(new_elements)
    
    def split(self, other):
        new_elements = []
        new_elements = self.elements.copy()
        for i in other.elements:
            if i not in new_elements:
                new_elements.append(i)
        return myset(new_elements)
    
    def xor(self, other):
        new_elements = []
        for i in self.elements:
            if i not in other.elements:
                new_elements.append(i)
        for i in other.elements:
            if i not in self.elements:
                new_elements.append(i)
        return myset(new_elements)
    


