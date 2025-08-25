t = int(input())

for _ in range(t):
    s = input()
    temp = ""
    for c in s:
        if (c.isalpha()):
            c = ' '
        temp += c
    nums = map(int, temp.split())
    print(max(nums))