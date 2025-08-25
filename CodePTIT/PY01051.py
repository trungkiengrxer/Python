t = int(input())
 
for _ in range(t):
    num = input()

    sum = 0
    for digit in num:
        sum += int(digit)

    print("YES" if str(sum) == str(sum)[::-1] and sum > 10 else "NO")