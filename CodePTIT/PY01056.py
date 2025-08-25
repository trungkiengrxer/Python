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

def is_valid(num):
    for i in range(len(num)):
        if not (i % 2 == 0 and int(num[i]) % 2 == 0 or i % 2 != 0 and int(num[i]) % 2 != 0):
            return False 
    if (is_prime(sum(num))):
        return True
    else:
        return False
    
t = int(input())
  
for _ in range(t):
    num = input()
    print("YES" if is_valid(num) else "NO")