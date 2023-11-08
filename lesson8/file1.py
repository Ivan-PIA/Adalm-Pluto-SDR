

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import adi 
import time

from scipy.fftpack import fft, ifft,  fftshift, ifftshift








fm = int(2000e6 + 2e6 * 4)
sdr = adi.Pluto("ip:192.168.3.1")
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 5000
sdr.rx_lo = fm
sdr.tx_lo = fm


#sdr.gain_control_mode_chan0 = 'manual' #fast_attack, slow_attack
#sdr.rx_hardwaregain_chan0 = 30.0
#sdr.tx_destroy_buffer()

#sdr.tx_cyclic_buffer = False

data = []
apl = 2**14
data += [apl + 1j * apl for i in range(0, 300)]
data += [1 + 1j*1 for i in range(0, 700)]


data1 = np.array([])
len_sample = 20

ampl_bit_1 = apl + 1j * apl
ampl_bit_0 = (apl/4) + (apl/4) * 1j


sample_bit_1 = [ampl_bit_1 for i in range(0, len_sample)]
sample_bit_0 = [ampl_bit_0 for i in range(0, len_sample)]


dist = 200

<<<<<<< HEAD
=======
ampl_bit_1 = 700# + 600j
ampl_bit_0 = 300# + 200j
len_msg_sinhr = 10
>>>>>>> refs/remotes/origin/main


def bit_to_char(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

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

def Decode_data1(data):
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
            

def message_sinhro(data):
    c1 = 0
    cc1 = 0
    for i in range(len(data)):
        if( (data[i].real < ampl_bit_1.real + dist and data[i].real > ampl_bit_1.real - dist) and\
             (data[i].imag < ampl_bit_1.imag + dist and data[i].imag > ampl_bit_1.imag - dist)
             
             ):
            c1 += 1
        else:
            c1 = 0
        
        if(c1 >= len_sample - 1):
           cc1 += 1 
        
        if(cc1 == len_msg_sinhr):
            return i
    
    return 'none'
    

def Decode_data(data):
    
    con_msg_sinhr = message_sinhro(data)
    if(con_msg_sinhr == 'none'):
        return ""
    
    decode = ""
    c1 = 0
    c0 = 0
    cc1 = 0
    for i in range(con_msg_sinhr, len(data)):
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
        
        if(c1 > len_sample - 1):
            decode += '1'
            c1 = 0
            cc1 += 1
        if(c0 > len_sample - 1):
            decode += '0'
            c0 = 0
            cc1 = 0
        if(cc1 >= len_msg_sinhr - 1):
            break
    return decode


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)



#непрерывное чтение
def ListenData(e):
    rx_data = sdr.rx()

    ax1.clear()
    plt.ylim(0, 1000)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    str_decode = Decode_data(abs(rx_data))
    #print("str_decode = ", str_decode)
    if(str_decode != ''):
        #plt.title(f"Полученные данные {str_decode}")
        
        len_msg = len(str_decode)
        a1 = int(len_msg / 8)
        print(a1)
        msg_string = bit_to_char(str_decode[: (a1 * 8)]);
        
        plt.title(f"Полученные данные { msg_string }")
        
        #for i in range(100):
            #print(str_decode)
    else:
        plt.title("Полученные данные {не удалось декодировать}")
    #plt.scatter(rx_data.real, rx_data.imag)
    #plt.plot(abs(rx_data))
    plt.plot(abs(rx_data))
    print(abs(rx_data))
    #time.sleep(5)

    
    
    
    

if(1):
    string = 'verstendet'








CON = 1


#Прослушивание сигнала
if(CON == 1):
    
    
    ani = animation.FuncAnimation(fig, ListenData, interval=100)
    plt.show()
# Отправка сигнала
elif(CON == 2):
    
    string_bit = char_to_bit(string)
    #print(string_bit)
    string_bit = "111111111" + string_bit + "111111111"
    print(f"{string} = {string_bit} ")
    
    data = bit_to_sample(string_bit)
    plt.plot(data)
    
<<<<<<< HEAD
    while(True):
        #print(1)
=======
    while(1):
>>>>>>> refs/remotes/origin/main
        sdr.tx(data)
        sdr.tx_destroy_buffer()
        #time.sleep(1)
        #print(1)
    

elif(CON ==3):
    string_bit = char_to_bit(string)
    print(f"{string} = {string_bit} ")
    data = bit_to_sample(string_bit)
    plt.plot(data)






















