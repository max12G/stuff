def root(number, n, eps = 1e-9):
    curr = number
    prev = number * 2
    while abs(curr - prev) > eps:
        prev = curr
        curr = 1 / n * ((n - 1) * curr + number / (curr ** (n - 1)))
    return curr