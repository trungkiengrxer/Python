t = int(input())

while t > 0:
    s1 = input()
    s2 = s1[::-1]

    is_valid = True
    for i in range(len(s1) - 1):
        if abs(ord(s1[i]) - ord(s1[i + 1])) != abs(ord(s2[i]) - ord(s2[i + 1])):
            is_valid = False
            break

    result = "YES" if is_valid else "NO"
    print(result)
    t -= 1
