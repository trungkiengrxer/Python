import matplotlib.pyplot as plt
import numpy
import random

class Signal:
    def __init__ (self, x, y, start):
        self.x = x
        self.y = y
        self.start = start

    def draw (self):
        self.x = numpy.arange(0 - self.start,0 - self.start + len(self.y))
        plt.stem(self.x, self.y)
        plt.show()
    
    def __add__(self, other):
        if (self.start == other.start):
            maxLength = max(len(self.y), len(other.y))
            if len(self.y) < maxLength:
                self.y += [0] * (maxLength - len(self.y))
            if len(other.y) < maxLength:
                other.y += [0] * (maxLength - len(other.y))
            result = [self.y[i] + other.y[i] for i in range(maxLength)]

            return Signal(self.x, result, self.start)
        
        else:
            maxStart = max(self.start, other.start)
            newStart = 2 * self.start + maxStart
            newSelfY =[]
            newOtherY = []
            if maxStart == self.start:
                newSelfY = self.y + [0] * (maxStart - other.start)
                newOtherY = [0] * (maxStart - other.start) + other.y
            else:
                newSelfY = [0] * (maxStart - self.start) + self.y
                newOtherY = other.y + [0] * (maxStart - self.start)
            
            result = [newSelfY[i] + newOtherY[i] for i in range(max(len(newOtherY),len(newSelfY)))]

            return Signal(self.x, result, maxStart)

            
if __name__ == "__main__":
    list1 = random.sample(range(-100, 100), 10)
    list2 = random.sample(range(-100, 100), 10)

    start1 = random.randint(-100, 100)
    start2 = random.randint(-100, 100)

    x1 = numpy.arange(len(list1))
    x2 = numpy.arange(len(list2))

    # list1 = [1, 2, 3, 4, 5, 6]
    # list2 = [1, 3, 1, 5, 1, 6]

    # start1 = 2
    # start2 = 1

    # x1 = numpy.arange(len(list1))
    # x2 = numpy.arange(len(list2))

    signal1 = Signal(x1, list1, start1)
    signal2 = Signal(x2, list2, start2)
    
    (signal1 + signal2).draw()
   