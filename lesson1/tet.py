import random
import matplotlib.pyplot as plt

import math
f=1
A=1
p=1

a = []
tim = []
c = []
t=0

for i in range(1000):
    
    c.append(A*math.cos(f*t+p))
    a.append(A*math.sin(f*t+p))
    t+=0.1
    tim.append(t)

plt.xlabel("time")
plt.ylabel("Ampl")

plt.plot(tim,a)
plt.plot(tim,c)
plt.show()