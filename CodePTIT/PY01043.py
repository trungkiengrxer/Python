from itertools import product


def gen_even_palindromes():
    result = []
    first = ['2', '4', '6', '8']
    digits = ['0', '2', '4', '6', '8']

    for len in (2, 4, 6):
        k = len // 2
        if (k == 1):
            for digit in first:
                result.append(int(digit + digit))
        else:
            for digit in first:
                for tail in product(digits, repeat=k - 1):
                    half = digit + "".join(tail)
                    full = half + half[::-1]
                    result.append(int(full))
    
    result.sort()
    return result

t = int(input())

even_palindromes = gen_even_palindromes()

for _ in range(t):
    n = int(input())

    for num in even_palindromes:
        if (num < n):
            print(num, end=" ")
    print()
