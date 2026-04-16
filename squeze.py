class SqueezeList:
    def __init__(self, base):
        self.base = self.squeeze(base)

    def squeeze(self, base):
        read = 0
        write = 0
        while read < len(base):
            char = base[read]
            st = read
            while read < len(base) and base[read] == char:
                read += 1
            count = read - st
            base[write] = char
            write += 1
            for digit in str(count):
                base[write] = digit
                write += 1
            
        base = base[:write]
        return base
    
    def unsqueeze(self):
        res = []
        ind = 0
        while ind < len(self.base):
            curr = self.base[ind]
            ind += 1
            s = ""
            while ind < len(self.base) and self.base[ind].isdigit():
                s += self.base[ind]
                ind += 1
            count = int(s)
            res.extend([curr] * count)
        self.base = res
        return self.base
    

import time
import itertools


def itertools_rle(data):
    return [(char, len(list(group))) for char, group in itertools.groupby(data)]

def itertools_unrle(data):
    res = []
    for char, count in data:
        res.extend([char] * count)
    return res

# Генерация данных: 1 миллион символов (группы по 10-100 символов)
import random
import string
test_data = "".join(random.choice(string.ascii_letters) * random.randint(10, 100) for _ in range(2000000))
print(f"Длина исходной строки: {len(test_data)} символов\n")

# Тест твоего класса
test_data = list(test_data)
start = time.time()
obj = SqueezeList(test_data)
compressed_data = obj.base
decompressed_data = obj.unsqueeze()
print(f"SqueezeList (твой): {time.time() - start:.4f} сек")

# Тест itertools
test_data = "".join(test_data)
start = time.time()
it_comp = itertools_rle(test_data)
it_uncomp = itertools_unrle(it_comp)
print(f"Itertools approach: {time.time() - start:.4f} сек")