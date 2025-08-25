def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while (i * i <= n):
        if n % i == 0:
            return False
        i += 2
    return True


def is_valid(n):
    if not is_prime(len(n)):
        return False

    count = 0
    for digit in n:
        if is_prime(int(digit)):
            count += 1

    return count > len(n) - count


t = int(input())

for _ in range(t):
    num = input()

    result = "YES" if is_valid(num) else "NO"
    print(result)
