import time

import adi
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.3.1")


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



t = text_to_bits("q")
str_modul = '1111111111'
t=str_modul+t+'1'

print(t)
ampl = 2**14
bit_1 = np.array([ampl+1j*ampl]*100)
c = np.array([0]*1000)
#f = np.concatenate([k,c])

bit_0 = np.array([ampl/10+ampl*1j/10]*100)



def AM():                    # функция амплитудной модуляции если встречается "1" увеличиваем амплитуду и если "0" уменьшаем
    data = []
    for i in range(len(t)):
        if t[i]=='0':
            data = np.concatenate([data,bit_0])
        elif t[i]=='1':
            data = np.concatenate([data,bit_1])
    return data

data = AM() # данные для передачи

#plt.plot(data)

d = []

for r in range(100):                #цикл для передачи данных и их принятие
    if (r==10 or r ==40 or r==80): # в какое время передавать данные
        sdr.tx(data)
    rx = sdr.rx()
    d = np.concatenate([d,abs(rx)]) # слияние массивов
str_after = '0000'
print(d)


for i in range(100):
    if d[i]>2800.0:
        str_after = str_after + '1'
    elif d[i]>1450.0 and d[i]<1900.0:
        str_after = str_after + '0'

print(type(d[1]))
print(str_after)
plt.xlabel('sample')
plt.ylabel('ampl')
plt.plot(d)
plt.show()    
