import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.3.1")


sdr.rx_lo = 2417000000
sdr.sample_rate = 1e6




N=1024

k=np.arange(0,N)
df=sdr.sample_rate/N
kf=k*df

for r in range(30):
    rx = sdr.rx()
    plt.clf()
    plt.stem(kf,abs(rx))
    plt.draw()
    plt.xlabel('Гц')
    plt.ylabel('$x[k]$')
    plt.pause(0.05)
    time.sleep(0.1)
plt.show()




