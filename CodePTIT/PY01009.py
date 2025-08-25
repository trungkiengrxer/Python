s = input()

lower_count = 0

for char in s:
    if char.islower():
        lower_count += 1

if (lower_count >= len(s) - lower_count):
    print(s.lower())
else: print(s.upper())