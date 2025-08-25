def prime(n):
    result = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            result.append(d)
            n //= d
        d += 1
    if n > 1:
        result.append(n)

    return result


t = int(input())

while t > 0:
    result = ["1"]
    n = int(input())

    primes = prime(n)

    freq = {}
    for p in primes:
        freq[p] = freq.get(p, 0) + 1

    for p in sorted(freq.keys()):
        count = freq[p]
        if count > 1:
            result.append(f"{p}^{count}")
        else:
            result.append(f"{str(p)}^1")
    t -= 1

    print(" * ".join(result))
