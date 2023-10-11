import time
import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.2.1")


sdr.rx_lo = 2400000000+2000000*3
sdr.sample_rate = 1e6
sdr.tx_lo = 2400000000+2000000*3

N=1024
t=np.arange(0,10,0.1) 
df=sdr.sample_rate/N
kf=t*df


#t=np.arange(0,N,1)
f=5


s=np.sin(2*np.pi*f*t)


plt.figure(1)
plt.plot(t,s)
tx = sdr.tx(s)
rx = sdr.rx()

plt.figure(2)
plt.plot(kf,abs(rx))
plt.show()




