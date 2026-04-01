from tqdm import tqdm
import sys
from time import perf_counter

class mydict:
    def __init__(self, items: list = []):
        self.items = items
        self.size = self.getsize(len(items))
        self.values = [None] * self.size
        self.keys = [None] * self.size
        self.used = len(items)
        if items:
            self.prepare_curr_vk()

    def getsize(self, n):
        s = 4
        while n > s:
            s += 4
        return s
    
    def get_vk(self):
        for i, k, v in enumerate(self.items):
            self.keys[i] = k
            self.values[i] = v
        del self.items
        return

    def prepare_curr_vk(self, keys, values):
        for key, val in zip(keys, values):
            h = hash(key)
            index = h ^ h >> 5
            index = index % self.size
            step = (index // self.size) % self.size | 1
            while not(self.keys[index] is None):
                index = (index + step) % self.size  
            self.keys[index] = key
            self.values[index] = val
        return 

    def __getitem__(self, key):
        h = hash(key)
        index = h ^ h >> 5
        index = index % self.size
        step = (index // self.size) % self.size | 1
        while self.keys[index] != key:
            index = (index + step) % self.size  
        return self.values[index]
    
    def resize(self):
        kef = self.size << 1
        self.size = kef
        keys_t, values_t = self.keys.copy(), self.values.copy()
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.prepare_curr_vk(keys_t, values_t)
        del keys_t, values_t
        return
    
    def add_item(self, key, value):
        if self.used / self.size > 0.66:
            self.resize()
        h = hash(key)
        index = h ^ h >> 5
        index = index % self.size
        step = (index // self.size) % self.size | 1
        while not(self.keys[index] is None):
            index = (index + step) % self.size   
            if self.keys[index] == key:
                self.values[index] = value
                return
        self.keys[index] = key
        self.values[index] = value
        self.items.append((key, value))
        self.used += 1
        return

    def pop(self, key):
        index = hash(key) % self.size
        while self.keys[index] != key:
            index += 1
        result = self.values[index]
        self.values[index] = None
        self.keys[index] = None
        self.used -= 1
        return result
    


