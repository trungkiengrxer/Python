import math


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while (i * i <= n):
        if n % i == 0:
            return False
        i += 2
    return True


t = int(input())

for _ in range(t):
    n = int(input())

    k = 0
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            k += 1

    result = "YES" if is_prime(k) else "NO"
    print(result)
