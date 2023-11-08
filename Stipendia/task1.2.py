import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import adi 
import time

from scipy.fftpack import fft, ifft,  fftshift, ifftshift



fm = int(900e6)
sdr = adi.Pluto("ip:192.168.2.1")
#sdr.sample_rate = 500000
sdr.rx_buffer_size = 10000
sdr.rx_lo = fm
sdr.tx_lo = fm

sdr.rx_buffer_size = 100000
sdr.tx_cyclic_buffer = True

 # 50 bit

Ns= 30
#bit = '01010101010101010110101010100101010101010101010100'

#bit_sinhro = 10*'1' + bit + 10 * '1'

num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 135 # 45, 135, 225, 315 град.
x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) #генерируем комплексные числа
samples = np.repeat(x_symbols, 16) # 16 сэмплов на символ
samples *= 2**14 #Повысим значения для наших сэмплов
print(x_symbols)

#print(x_int)
plt.plot(samples)
plt.show()