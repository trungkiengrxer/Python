import numpy
import matplotlib.pyplot as plt
import random
import math

def init(size, frameLength):
    num = [random.randint(1, 100) for _ in range (size)]
    return num

def frameList(num, size, frameLength, frameOverlap):
    frameList = []
    for i in range(0, size, frameLength - frameOverlap):
        frameList.append(num[i : i + frameLength])
        if len(frameList[-1]) < frameLength:
            for i in range(len(frameList[-1]), frameLength):
                frameList[-1].append(0)
    return frameList

def calculateE(frameList):
    e = []
    for i in frameList:
        sum = 0
        for j in i:
            sum += math.pow(j, 2)
        e.append(sum)
    return e

def calculateM(frameList):
    m = []
    for i in frameList:
        sum = 0
        for j in i:
            sum += math.fabs(j)
        m.append(sum)
    return m

def printFrame(frameList, eList, mList):
    for i in range(len(frameList)):
        print(frameList[i], eList[i], mList[i], sep = " ")


size = int(input())
frameLength = int(input())
overlap = float(input())

num = init(size, frameLength)
num = init(size, frameLength)

print("Original List", num, sep = " ")
print("\n")

frameOverlap = int(frameLength * overlap)
frameResult = frameList(num, size, frameLength, frameOverlap)
eResult = calculateE(frameResult)
mResult = calculateM(frameResult)
printFrame(frameResult, eResult, mResult)