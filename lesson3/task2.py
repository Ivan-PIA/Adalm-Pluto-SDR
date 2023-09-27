import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.2.1")


sdr.rx_lo = 2417000000


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
    if rx.imag[r]>2000:
        time.sleep(2)

plt.show()
