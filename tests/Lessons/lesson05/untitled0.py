import matplotlib.pyplot as plt
import numpy as np

N=100





fc1=10 # Частота косинуса 

t1=np.arange( 0, 1, 0.0000001) 
x1=np.cos(2*np.pi*fc1*t1) 

plt.plot(t1,x1)
plt.show()