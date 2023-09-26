import numpy as np
import random
import matplotlib.pyplot as plt
import time



def time_sort_numpy(n):
    a = np.random.sample(n)
    start = time.time()
    np.sort(a)
    end = time.time() - start

    return end

def time_sort_list(n):
    b = []
    for i in range(n):
        b.append(random.random())
    start = time.time()
    b.sort()
    end = time.time() - start
    return end


time_list = []
time_numpy = []
count_el = []


for i in range(10,5000000,800000):
    time_list.append(time_sort_list(i))
    time_numpy.append(time_sort_numpy(i))
    count_el.append(i)

plt.plot(time_list,count_el,label='List')
plt.plot(time_numpy,count_el, label='Numpy')
plt.xlabel("Time, s")
plt.ylabel("Count elements")
plt.yticks(np.arange(10, 5000000, 500000))#шаг
plt.legend(fontsize=14)
plt.show()
    

#print("time Numpy:",time_sort_numpy())
#print("time List:",time_sort_list())




