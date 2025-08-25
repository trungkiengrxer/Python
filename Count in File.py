from collections import defaultdict
import re

def countDigrams(lines, digramsFreq):
    wordsSet = lines.lower().strip().split()
    for i in range (len(wordsSet) - 1):

        for char in wordsSet[i]:
            if not char.isalpha():
                wordsSet[i] = wordsSet[i].replace(char, "")
        for char in wordsSet[i + 1]:
            if not char.isalpha():
                wordsSet[i + 1] = wordsSet[i + 1].replace(char, "")

        word = wordsSet[i] + " " + wordsSet[i + 1]
        if word in digramsFreq:
            digramsFreq[word] += 1
        else:
            digramsFreq[word] = 1

with open("hihi.txt", "r", encoding = "utf-8") as fobj:
    digramsFreq = defaultdict(int)
    for lines in fobj:
        countDigrams(lines, digramsFreq)

with open("output.txt", "w", encoding = "utf-8") as out:
    for key, value in digramsFreq.items():
        out.write(f"{key} : {value}\n")