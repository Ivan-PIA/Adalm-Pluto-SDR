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
   
    c.append(A*math.cos(f*t+p))# сгенерировали массив значений по синусоидальному закону
    a.append(A*math.sin(f*t+p))
    t+=0.1
    tim.append(t)

plt.xlabel("time")
plt.ylabel("Ampl")

plt.plot(tim,a,'r')
plt.plot(tim,c,'c')
plt.show()