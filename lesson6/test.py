import matplotlib.pyplot as plt
import numpy as np







k = np.array([2**13+1.j*2**13]*300)
c = np.array([0]*700)
f = k+c
plt.plot(f)

plt.show()