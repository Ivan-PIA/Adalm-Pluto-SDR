import matplotlib.pyplot as plt
import numpy as np

N=100

fc=10000

t=np.arange(0,1000) 
x=np.sin(2*np.pi*fc*t)

plt.plot(t,x)
plt.show()