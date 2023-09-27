import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.2.1")


sdr.rx_lo = 2417000000

s=0
for r in range(30):
    rx = sdr.rx()
    plt.clf()
    plt.plot(rx.real)
    plt.plot(rx.imag)
    plt.draw()
    plt.xlabel('time')
    plt.ylabel('ampl')
    plt.pause(0.05)
    time.sleep(0.1)
    for i in range(len(rx.imag)):
       s+=rx.imag[i] 
    sred=s/len(rx.imag)  
    if rx.imag[r]>sred:
        time.sleep(2)
    print(sred)

plt.show()
