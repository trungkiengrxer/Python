with open('test.txt', 'w') as f:
    for i in range(2 * 1000, 2, -1):
        f.write(f"{i} ")