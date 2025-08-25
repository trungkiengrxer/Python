import math

l, r = map(int, input().split())

for a in range(l, r + 1):
    for b in range(a + 1, r + 1):
        for c in range(b + 1, r + 1):
            if math.gcd(a, b) == 1 and math.gcd(c, b) == 1 and math.gcd(a, c) == 1:
                print(f"({a}, {b}, {c})", end="\n")
