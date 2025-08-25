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
    a, b = map(int, input().split())

    gcd = math.gcd(a, b)
    s = sum(int(digit) for digit in str(gcd))

    result = "YES" if is_prime(s) else "NO"
    print(result)
