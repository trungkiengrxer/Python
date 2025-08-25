t = int(input())

while t > 0:
    s = input()

    result = ""
    freq = {}

    i = 0
    n = len(s)
    count = 1
    for i in range(n):
        if i < n - 1 and s[i] == s[i + 1]:
            count += 1
        else:
            result += (str(count) + s[i])
            count = 1
    
    print(result)
    t -= 1
