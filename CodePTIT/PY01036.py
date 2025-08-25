t = int(input())

for _ in range(t):
    n = int(input())

    sum = 0
    i = 2 if n % 2 == 0 else 1

    while i <= n:
        sum += 1 / i
        i += 2
    print(f"{sum:.6f}")