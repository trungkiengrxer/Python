t = int(input())

for _ in range(t):
    n = int(input())

    a = list(map(int, input().split()))
    a.sort()
    count = 0

    for i in range(n - 2):
        l, r = i + 1, n - 1
        while (l < r):
            s = a[i] + a[l] + a[r]
            if s == 0:
                count += 1
                l += 1
                r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    
    print(count)