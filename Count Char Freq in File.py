with open("hihi.txt", "r", encoding = "utf-8") as fobj: 
    """Dem tan suat xuat hien cua cac ki tu trong file """       
    def countCharFreq(lines, count):
        for char in lines:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1
    
    count = {}
    for lines in fobj:
        countCharFreq(lines, count)

    sortedCount = dict(sorted(count.items()))

    for key, value in sortedCount.items():
        if key.isalnum():
            print(key, value, sep = " : ")