import numpy as np
import matplotlib.pyplot as plt


a = np.array([1, 1, 1, -1, 1])
b = np.correlate(a,a,'full')
print(b)
plt.plot(b)
plt.show()