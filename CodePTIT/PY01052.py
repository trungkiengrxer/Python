import math

def is_prime(n):
    if (n < 2):
        return False
    
    if (n % 2 == 0):
        return n == 2
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if (n % i == 0):
            return False
    
    return True

def sum(n):
    sum = 0
    for digit in n:
        sum += int(digit)
    return sum

t = int(input())
 
for _ in range(t):
    num = input()
    print("YES" if is_prime(sum(num)) else "NO")