import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.2.1")


sdr.rx_lo = int(2000e6 + 2e6 * 3)
sdr.tx_lo = int(2000e6 + 2e6 * 3)
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 10000
sdr.tx_cyclic_buffer = False


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):                      # перевод из текста в биты
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



word = 'andrey'


bits = text_to_bits(word)
print(bits[1])
bit_num_samples = 20
bits = bits

bit_1 = np.array([2**14 + 1j * 2**14]*bit_num_samples,dtype = "complex_")
bit_0 = np.array([1 +1j * 1]*bit_num_samples,dtype = "complex_")
print(1)
def AM():                    
    data = []
    print(1)
    for i in range(len(bits)):
        print(1)
        if bits[i]=='0':
            data = np.concatenate(data,bit_0)
        elif bits[i]=='1':
            data= np.concatenate(data,bit_1)
    return data

plt.plot(AM())




