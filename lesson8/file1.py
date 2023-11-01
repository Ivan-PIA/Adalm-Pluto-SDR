

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import adi 
import time

from scipy.fftpack import fft, ifft,  fftshift, ifftshift








fm = int(2000e6 + 2e6 * 4)
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 10000
sdr.rx_lo = fm
sdr.tx_lo = fm




data = []
apl = 2**14
data += [apl + 1j * apl for i in range(0, 300)]
data += [1 + 1j*1 for i in range(0, 700)]


data1 = np.array([])
len_sample = 30

ampl_bit_1 = apl + 1j * apl
ampl_bit_0 = (apl/4) + (apl/4) * 1j


sample_bit_1 = [ampl_bit_1 for i in range(0, len_sample)]
sample_bit_0 = [ampl_bit_0 for i in range(0, len_sample)]


dist = 30




#строку в бинарный режим
def char_to_bit(char):
    return ''.join(format(ord(i), '08b') for i in char)
# бинарный код в сэмплы
def bit_to_sample(byte_str):
    sample_code = []
    
    for i in range(len(byte_str)):
        if(byte_str[i] == '0'):
            sample_code += sample_bit_0
        elif( byte_str[i] == '1'):
            sample_code += sample_bit_1
    return sample_code

def Decode_data(data):
    decode = ""
    c1 = 0
    c0 = 0
    for i in range(len(data)):
        #0
        
        if( (data[i].real < ampl_bit_0.real + dist and data[i].real > ampl_bit_0.real - dist) and\
             (data[i].imag < ampl_bit_0.imag + dist and data[i].imag > ampl_bit_0.imag - dist)
             
             ):
            c0 += 1
            c1 = 0
            pass
        else:
            c0 = 0
        #1
        if( (data[i].real < ampl_bit_1.real + dist and data[i].real > ampl_bit_1.real - dist) and\
             (data[i].imag < ampl_bit_1.imag + dist and data[i].imag > ampl_bit_1.imag - dist)
             
             ):
            c1 += 1
            c0 = 0
            pass
        else:
            c1 = 0
        
        if(c1 > 20):
            decode += '1'
            c1 = 0
        if(c0 > 20):
            decode += '0'
            c0 = 0
    return decode
            

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)



#непрерывное чтение
def ListenData(e):
    rx_data = sdr.rx()

    ax1.clear()
    plt.ylim(-2000, 2000)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    str_decode = Decode_data(rx_data)
    #print("str_decode = ", str_decode)
    if(str_decode != ''):
        plt.title(f"Полученные данные {str_decode}")
    else:
        plt.title("Полученные данные {не удалось декодировать}")
    #plt.scatter(rx_data.real, rx_data.imag)
    plt.plot(rx_data)
    
    
    
    

if(1):
    string = 'verstended'








CON = 2


#П`рослушивание сигнала
if(CON == 1):
    
    
    ani = animation.FuncAnimation(fig, ListenData, interval=100)
    plt.show()
# Отправка сигнала
elif(CON == 2):
    
    string_bit = char_to_bit(string)
    print(f"{string} = {string_bit} ")
    string_bit = '11111111111111111111111111111111111111111111111111111111111111111111111111'
    data = bit_to_sample(string_bit)
    plt.plot(data)
    
    while(True):
        print(1)
        sdr.tx(data)
    

elif(CON ==3):
    string_bit = char_to_bit(string)
    print(f"{string} = {string_bit} ")
   
    data = bit_to_sample(string_bit)
    plt.plot(data)






















