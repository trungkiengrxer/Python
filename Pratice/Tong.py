import sys
input = sys.stdin.read


data = input().split()
index = 0

t = int(data[index])
index += 1

for i in range(1, t + 1):
    d = int(data[index])
    index += 1
    a = []
    for _ in range(d):
        a.append([int(data[index]), int(data[index + 1]), int(data[index + 2])])
        index += 3

    dp = a[0]

    for j in range(1, d):
        a1, a2, a3 = a[j]
        p1, p2, p3 = dp
        dp[0] = a1 + max(p2, p3)
        dp[1] = a2 + max(p1, p3)
        dp[2] = a3 + max(p1, p2)

    result = max(dp)
    print(f'Case #{i}: {result}')
