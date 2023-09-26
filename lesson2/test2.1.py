import numpy as np
import matplotlib.pyplot as plt

#%matplotlib inline




n = 40
# time vector
t = np.linspace(0, 1, n, endpoint=True)
# sine wave
x = np.sin(np.pi*t) + np.sin(2*np.pi*t) + np.sin(3*np.pi*t) + np.sin(5*np.pi*t)

fig = plt.figure(figsize=(16, 5), dpi=100)
plt.plot(t, x)
plt.show()