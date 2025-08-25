a, k, n = map(int, input().split())

result = []
start = (a // k + 1) * k
i = 1
while start <= n:
    result.append(start - a)
    start += k

if len(result) == 0:
    print("-1")
else:
    print(" ".join(map(str, result)))
