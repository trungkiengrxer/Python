import math

n, k = map(int, input().split())

count = 0
for num in range(10 ** (k - 1), 10 ** k):
    if math.gcd(num, n) == 1:
        count += 1
        end_char = " " if count % 10 != 0 else "\n"
        print(num, end=end_char)
