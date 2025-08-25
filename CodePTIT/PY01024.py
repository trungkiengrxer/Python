def is_valid(n):
    sum = int(n[-1])
    for i in range(len(n) - 1):
        sum += int(n[i])
        if (abs(int(n[i]) - int(n[i + 1])) != 2):
            return False
        
    return sum % 10 == 0

t = int(input())

for _ in range(t):
    n = input()

    result = "YES" if is_valid(n) else "NO"
    print(result)

