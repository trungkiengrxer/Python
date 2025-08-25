t = int(input())

for _ in range(t):
    n = int(input())

    if n % 7 == 0:
        print(n)
        continue
    
    found = False
    a = n
    b = int(str(n)[::-1])
    sum = 0
    for _ in range(1000):
        sum = a + b
        a = sum
        b = int(str(sum)[::-1])

        if sum % 7 == 0:
            found = True
            break

    result = sum if found else -1
    print(result)