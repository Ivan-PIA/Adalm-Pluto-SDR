import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.3.1")


sdr.rx_lo = 2000000000
sdr.tx_lo = 2000000000
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 10000



def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



t = text_to_bits("q")
print(t)
k = np.array([2**13+1j*2**13]*100)
c = np.array([0]*1000)
f = np.concatenate([k,c])





def AM():
    data = []
    for i in range(len(t)):
        if t[i]=='0':
            data = np.concatenate([data,k])
        else:
            data = np.concatenate([data,k])
    return data    

data = AM()
#plt.plot(data)
d = []

for r in range(100):
    if r>50 and r<56:
        sdr.tx(data)
    rx = sdr.rx()
    d = np.concatenate([d,abs(rx)])

plt.plot(d)

plt.show()    
