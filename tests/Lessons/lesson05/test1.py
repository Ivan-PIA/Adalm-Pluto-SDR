import time
import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.2.1")

sdr.rx_lo = 2400000000 + 2000000 * 3
sdr.tx_lo = 2400000000 + 2000000 * 3
sdr.sample_rate=1e6


# Create a sinewave waveform
fc = 10000
ts = 1/float(sdr.sample_rate)
t = np.arange(0, fc*ts, ts)
i = np.sin(2*np.pi*t*fc) * 2**14
q = np.cos(2*np.pi*t*fc) * 2**14
#samples = i + 1j*q

#destroy buffer
sdr.tx_destroy_buffer()

# Start the transmitter
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.tx(i)
rx = sdr.rx()
print(type(i[1]))
plt.figure(1)
plt.plot(i)
plt.figure(2)
plt.plot(rx)
plt.show()