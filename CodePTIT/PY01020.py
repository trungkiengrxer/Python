t = int(input())

while t > 0:
    num = input()

    if num[-2::1] == "86":
        print("YES")
    else:
        print("NO")

    t -= 1
