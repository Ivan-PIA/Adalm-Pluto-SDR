import numpy as np
import random
import matplotlib.pyplot as plt
import time





#a = np.random.randint(1,50000)
#b = np.random.randint(1,50000)
data_time = []
arr1 = []

def time_sort_numpy():
    #a = np.random.sample(5000000)
    for i in range(10,5000000,200000):
        
        
        a = np.random.sample(5000000)
        start = time.time()
        
        np.sort(a)

        end = time.time() - start
        data_time.append(end)
        arr1.append(i)
        
    return end

time_sort_numpy()
plt.plot(arr1,data_time)
plt.show()
