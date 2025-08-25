t = int(input())


def is_valid(n):
    if (len(n) < 3):
        return False
    point_1 = 0

    for i in range(len(n) - 1):
        if (int(n[i]) >= int(n[i + 1])):
            point_1 = i
            break

    point_2 = 0
    for i in range(len(n) - 2, -1, -1):
        if (int(n[i]) <= int(n[i + 1])):
            point_2 = i
            break

    point_2 += 1
    if (point_2 != point_1):
        return False
    return True


for _ in range(t):
    n = input()
    print("YES" if is_valid(n) else "NO")
