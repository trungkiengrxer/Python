import sys

P = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_."
pos = {ch: i for i, ch in enumerate(P)}

result = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line == "0":
        break
    k_str, s = line.split()
    k = int(k_str)

    if k == 0:
        break
    encoded = "".join(P[(pos[c] + k) % 28] for c in s)
    result.append(encoded[::-1])

print("\n".join(result))
