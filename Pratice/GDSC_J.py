max = 1000001
prime = [True] * max

def sieve():
    prime[0] = prime[1] = False
    lim = int(max ** 0.5)
    for i in range(2, lim + 1):
        if prime[i]:
            for j in range(i * i, max, i):
                prime[j] = False

def prime_factor(n):
    map = {}
    lim = int(n ** 0.5)
    for i in range(2, lim + 1):
        if prime[i] > n: break
        while (n % prime[i] == 0):
            map[prime[i]] += 1
            n //= prime[i]
        lim = int(n ** 0.5)
    
    if n > 1: map[n] += 1
    return map



sieve()
import math
t = int(input())
for test_case in range(1, t + 1):
    result = 0
    n = int(input())
    a = list(map(int, input().split()))
    map_list = []
    for num in a:
        map_list.append(prime_factor(num))
    for map in map_list:
        for key in map:
            result += map[key]
    
    print(f'Case #{test_case}: {result}')
