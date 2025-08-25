t = int(input())

for _ in range(t):
    num = input()

    result = 1
    for digit in num:
        if digit == '0':
            continue
        result *= int(digit)
        
    print(result)