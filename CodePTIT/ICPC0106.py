t = int(input())

def convert_to_int(n):
    if n == 0:
        return '0'
    digits = []
    while n:
        digits.append(str(n % 4))
        n //= 4
    return "".join(reversed(digits))

for _ in range(t):
    b = int(input())
    s = input()

    if (b == 2) :
        print(s)

    n = int(s, 2)
    if (b == 8):
        print(format(n, 'o'))
    elif b == 16:
        print(format(n, 'X'))
    elif b == 4:
        print(convert_to_int(n))