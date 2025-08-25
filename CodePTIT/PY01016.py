t = int(input())

while t > 0:
    s = input()

    result = ""
    for i in range(len(s)):
        if s[i].isnumeric():
            result += (s[i - 1] * int(s[i]))
    print(result)
    t -= 1