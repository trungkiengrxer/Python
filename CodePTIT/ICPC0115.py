t = int(input())

fact = [1] * 10
for i in range(1, 10):
    fact[i] = fact[i - 1] * i

for _ in range(t):
    num = input()

    sum = 0
    for digit in num:
        sum += fact[int(digit)]
    print("Yes" if sum == int(num) else "No")
