import adi
import time
import matplotlib.pyplot as plt
import numpy as np


sdr = adi.Pluto("ip:192.168.3.1")


sdr.rx_lo = int(2000e6)
sdr.tx_lo = int(2000e6)
sdr.sample_rate = 1e6

sdr.rx_buffer_size = 100000
sdr.tx_cyclic_buffer = False


fc =10


t=np.arange(0,1,1/sdr.sample_rate)

i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
#samples = i + 1j * q


# plt.xlabel("time, s")
# plt.ylabel("Ampl")
# plt.title("Отправленый сигнал")
# #plt.subplot(1,2,1)
# #plt.plot(t,np.real(samples))
# #plt.plot(t,np.imag(samples))

# plt.xlabel("time, s")
# plt.ylabel("Ampl")
# plt.title("Принятый сигнал")


rx = sdr.rx()

#Генерируем QPSK-модулированный сигнал, 16 сэмплов на символ
num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 135 # 45, 135, 225, 315 град.
x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) #генерируем комплексные числа
samples = np.repeat(x_symbols, 16) # 16 сэмплов на символ
samples *= 2**14 #Повысим значения для наших сэмплов

while 1:
    sdr.tx(samples)
    print(1)




