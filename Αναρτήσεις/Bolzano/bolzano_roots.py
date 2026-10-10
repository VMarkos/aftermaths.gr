def bisection(f, a, b, epsilon): # f: real-valued function, a, b ,epsilon real numbers.
    if (b <= a) or f(a) * f(b) >= 0:
        return None
    c = (a + b) / 2
    while (b - a > epsilon and f(c) != 0):
        if (f(c) < 0):
            a = c
        else:
            b = c
        c = (a + b) / 2
    return c

def f1(x):
    return x ** 3 + x + 1

if __name__ == '__main__':
    f = f1
    a = -1
    b = 0
    epsilon = 10 ** (-6)
    print(bisection(f, a, b, epsilon))