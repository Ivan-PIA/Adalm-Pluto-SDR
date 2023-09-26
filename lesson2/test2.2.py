import numpy as np
import random
import matplotlib.pyplot as plt
import time



def time_sort_numpy():
    a = np.random.sample(5000000)
    start = time.time()
    np.sort(a)
    end = time.time() - start

    return end

def time_sort_list():
    b = []
    for i in range(5000000):
        b.append(random.random())
    start = time.time()
    b.sort()
    end = time.time() - start
    return end


    

print("time Numpy:",time_sort_numpy())
print("time List:",time_sort_list())




