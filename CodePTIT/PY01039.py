def is_beautiful_num(n):

    check_set = set()
    for digit in n:
        check_set.add(digit)

    if len(check_set) > 2 or len(check_set) < 2:
        return False

    for i in range(len(n) - 2):
        if abs(int(n[i]) - int(n[i + 1])) != abs(int(n[i + 1]) - int(n[i + 2])):
            return False

    return True


t = int(input())

for _ in range(t):
    n = input()
    print("YES" if is_beautiful_num(n) else "NO")
