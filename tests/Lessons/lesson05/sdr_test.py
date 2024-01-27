import time

import adi
import matplotlib.pyplot as plt
import numpy as np
from .context import init_rx, standart_settings

sdr = standart_settings("ip:192.168.2.1", 1000000)
init_rx("ip:192.168.2.1", 1000000, 2000000000, 70)
# sdr = adi.Pluto("ip:192.168.2.1")


# sdr.rx_lo = 2400000000 + 2000000 * 3
# sdr.tx_lo = 2400000000 + 2000000 * 3
# sdr.sample_rate=1e6




N=1024
fc=4

k=np.arange(0,1,0.0001)
k = k / fc

s = np.sin(2*np.pi*fc*k) 
print(s)
plt.figure(1)
plt.plot(s)
plt.figure(2)
for r in range(30):
    
    sdr.tx(s)
    rx = sdr.rx()
    plt.clf()
    plt.plot(rx)
    plt.draw()
    plt.xlabel('Гц')
    plt.ylabel('$x[k]$')
    plt.pause(0.05)
    time.sleep(0.1)
plt.show()
