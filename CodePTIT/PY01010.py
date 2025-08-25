t = int(input())

while t > 0:
    num = input()

    num1 = num[0] + num[1]
    num2 = num[-2] + num[-1]

    if num1 == num2: print("YES")
    else: print("NO")
    
    t -= 1