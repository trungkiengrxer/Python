line = input()

a = ''
b = ''
c = ''

a = int(line[0])
b = int(line[4])
c = int(line[len(line) - 1])

if a + b == c:
    print("YES")
else:
    print("NO")
