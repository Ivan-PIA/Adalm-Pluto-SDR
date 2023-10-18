

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.3.1")


sdr.rx_lo = 2000000000
sdr.tx_lo = 2000000000
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 1000


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



t = text_to_bits('q')

time = np.arange(0,len(t))  
s = np.sin(2*np.pi*time)

def bits_to_ampl():
    for i in range(len(t)):
        if t[i] == '0':
            s[i]*=300
        
    
plt.plot(time,s)
plt.show()
#w = text_from_bits(t)
#print(t,w)