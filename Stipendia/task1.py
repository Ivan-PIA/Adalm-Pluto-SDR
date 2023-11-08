import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import adi 
import time

from scipy.fftpack import fft, ifft,  fftshift, ifftshift



fm = int(1200e6)
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = 1e6

sdr.rx_lo = fm
sdr.tx_lo = fm

sdr.rx_buffer_size = 100000
sdr.tx_cyclic_buffer = False


def gen_QPSK():          # Генерация QPSK сигнала  
    Ns= 30 # кол-во семплов на бит
   

    num_symbols = 50
    x_int = np.random.randint(0, 4, num_symbols) 
    #sihro_1 = np.array([1]*10)
    #x_int = np.append(x_int, [1]*10)
    #x_int = np.insert(x_int,0,[1]*10)
    bit = ''
    for i in range(len(x_int)):
        if x_int[i]==0:
            bit+='00'
        if x_int[i]==1:
            bit+='01'
        if x_int[i]==2:
            bit+='10' 
        if x_int[i]==3:
            bit+='11'
    print(x_int)
    print(bit)

    x_degrees = x_int*360/4.0 + 135 
    x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
    x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) 
    samples = np.repeat(x_symbols, Ns) 
    samples *= 2**14 

    
    X = fft(samples)

    plt.figure(1)
    plt.grid()
    plt.title('Временное представление')
    plt.scatter(samples.real,samples.imag)
    plt.figure(2)
    plt.title('Частотное представление')
    plt.plot(X)

    return samples


def Txer(data): # Отправка данных
    while 1:
        sdr.tx(data)
        sdr.tx_destroy_buffer()
        print(1)

def listen_efir(data):   # Прием данных в реальном времени
   
    for r in range(50):
        sdr.tx(data)
        sdr.tx_destroy_buffer()
        rx_data = sdr.rx()
        plt.clf()
        plt.scatter(rx_data.real,rx_data.imag)
        plt.draw()
        plt.xlabel('Гц')
        plt.ylabel('$x[k]$')
        plt.pause(0.05)
        time.sleep(0.1)
        
#Txer(gen_QPSK())
listen_efir(gen_QPSK())
plt.show()


