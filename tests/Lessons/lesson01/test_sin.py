import matplotlib.pyplot as plt
#import pylab as plt
import math


data = []
xdata = []
ydata = []
data_time = []
i = 0
while(i < 10):
    
   
    data_time.append(i)
    data.append(math.sin(i))
    ydata.append(complex(i, math.sin(i)))
    i+=0.1
print("len = ", len(data))
for i in ydata:
    print(i)
    

plt.plot(data_time, data, c = 'g')#, marker='x', label='1')
plt.plot(data, data_time, c = 'g')#, marker='x', label='1')

plt.show()


