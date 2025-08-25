from itertools import product

n = int(input())

result = []
for len in range(3, n + 1):
    for tup in product("ABC", repeat=len):
        a = tup.count('A')
        b = tup.count('B')
        c = len - a - b
        if a >= 1 and b >= 1 and c >= 1 and a <= b <= c:
            result.append("".join(tup))

print("\n".join(result))