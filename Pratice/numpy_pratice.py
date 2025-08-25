import numpy

a = numpy.array([[numpy.random.randint(1, 10) for j in range(10)] for i in range(10)])
b = numpy.array([[numpy.random.randint(1, 10) for j in range(10)] for i in range(10)])

print(a)
print(b)


c = numpy.dot(a, b)
print(c)
