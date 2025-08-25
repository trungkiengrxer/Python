def is_valid(num):
    if len(num) % 2 == 0:
        return False
    if (num[0] == num[1]):
        return False
    for i in range(0, len(num) - 3, 2):
        if (num[i] != num[i + 2]):
            return False
    return True

t = int(input())
 
for _ in range(t):
    num = input()
    print("YES" if is_valid(num) else "NO")