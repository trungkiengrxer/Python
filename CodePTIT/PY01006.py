t = int(input())

while t > 0:
    num = input()

    is_valid = True

    for digit in num:
        if not (digit == '4' or digit == '7'):
            is_valid = False
            break
    
    if is_valid: print("YES")
    else: print("NO")
    t -= 1