def replace_all(s, old, new):
    if old == new:
        return s
    return s.replace(old, new)


t = int(input().strip())

for _ in range(t):
    p, q = map(str, input().split())
    if p > q:
        p, q = q, p

    x1 = input()
    if len(x1.split()) > 1:
        x1, x2 = x1.split()
    else:
        x2 = input()

    min_x1 = replace_all(x1, q, p)
    min_x2 = replace_all(x2, q, p)

    max_x1 = replace_all(x1, p, q)
    max_x2 = replace_all(x2, p, q)

    print(f"{int(min_x1) + int(min_x2)} {int(max_x1) + int(max_x2)}")
