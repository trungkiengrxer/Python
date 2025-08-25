n = int(input())

for _ in range(n):
    num = input()
    result = "YES" if num[0] == num[-1] else "NO"
    print(result)