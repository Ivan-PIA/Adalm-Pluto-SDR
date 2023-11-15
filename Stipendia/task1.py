import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import adi 
import time

from scipy.fftpack import fft, ifft,  fftshift, ifftshift



fm = int(1200e6)
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 1000
sdr.rx_lo = fm
sdr.tx_lo = fm

sdr.rx_buffer_size = 100000
sdr.tx_cyclic_buffer = False

# 50 bit
def gen_QPSK():
    Ns= 30
   

    num_symbols = 50
    x_int = np.random.randint(0, 4, num_symbols) 
    rand_bit = np.random.choice(2,50)
    
    rand_bit = np.insert(rand_bit,0,[1]*10)
    print("rand _bit",rand_bit)

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
    
    pr_bit = join(rand_bit)
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


def Txer(data):
    while 1:
        sdr.tx(data)
        sdr.tx_destroy_buffer()
        print(1)


def get_rx():
    rx_data = sdr.rx()

    pass


def listen_efir(data):
   
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
#listen_efir(gen_QPSK())
gen_QPSK()
plt.show()