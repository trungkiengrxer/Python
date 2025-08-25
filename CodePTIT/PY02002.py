t = int(input())

fibo = [1] * 94
fibo[0] = 0
fibo[1] = 1
for i in range(2, 94):
    fibo[i] = fibo[i - 1] + fibo[i - 2]

for _ in range(t):
    a, b = map(int, input().split())
    for i in range(a, b + 1):
        print(fibo[i], end=" ")
    print()
