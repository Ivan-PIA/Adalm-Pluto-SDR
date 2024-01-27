import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.fftpack import fft, ifft,  fftshift, ifftshift



# 50 bit
def gen_QPSK():
    Ns= 30
   

    num_symbols = 50
    x_int = np.random.randint(0, 4, num_symbols) 
    #rand_bit = np.random.choice(4,25)
    
    #rand_bit = np.insert(rand_bit,0,[1]*10)
    #print("rand _bit",rand_bit)

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
    
    bit = 10*"1"+bit
    print(bit)
    b = re.findall(r'\d\d', bit)
    for i in range(len(b)):
        b[i]=int(b[i])
    #print(b)
    print(np.unique(b))
    b = np.array(b)
    x_degrees = (b*90) + 135
    x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
    x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) 
    samples = np.repeat(x_symbols, Ns) 
    print(samples)
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



gen_QPSK()
plt.show()