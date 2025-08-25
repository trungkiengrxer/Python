import numpy as np
import matplotlib.pyplot as plt

p = np.linspace(1e-100, 1 - 1e-100, 1000000)
result = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

plt.plot(p, result)
plt.xlabel('p')
plt.ylabel('H(p)')
plt.title('Entropy function')
plt.show()
