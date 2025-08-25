def is_valid(num):
    for digit in num:
        if digit != '0' and digit != '1' and digit != '2':
            return False

    return True

t = int(input())
 
for _ in range(t):
    num = input()
    print("YES" if is_valid(num) else "NO")
    
