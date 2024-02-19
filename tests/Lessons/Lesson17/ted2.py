import scipy. io as sp
from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM, text_from_bits, text_to_bits
import matplotlib.pyplot as plt
import numpy as np
import statistics



def TED(data):
    err = np.zeros(len(data)//10, dtype = "complex_")
    ted_plot = np.zeros(20, dtype = "complex_")
    data = np.roll(data,-2)
    #err = []
    buffer = np.zeros(len(data)//10, dtype = "complex_")
    nsp = 10
    for n in range(0,20):
        for ns in range(0,len(data)-(2*nsp+9),nsp):
            real = (data.real[n+ns] - data.real[n+nsp+ns]) * data.real[n+nsp//2+ns]
            imag = (data.imag[n+ns] - data.imag[n+nsp+ns]) * data.imag[n+nsp//2+ns]
            err[ns//nsp] = real + imag 
            buffer[ns//nsp] = err[ns//nsp]    
        ted_plot[n] = np.mean(buffer)
        buffer.fill(0)
        #plt.plot(err) 
        #plt.show()
    return ted_plot

def TED1(data):
    err = np.zeros(len(data)//10, dtype = "complex_")
    data = np.roll(data,-2)
    nsp = 10
    
    for ns in range(0,len(data)-(2*nsp+9),nsp):
        real = (data.real[ns] - data.real[nsp+ns]) * data.real[nsp//2+ns]
        imag = (data.imag[ns] - data.imag[nsp+ns]) * data.imag[nsp//2+ns]
        err[ns//nsp] = real + imag 

    return err

def Get_Index(qpsk, index): # вычленяет семпл выбранный глазковой диаграммой 
    decode_symbol = []
    for i in range(index,len(qpsk),10):
        #print()
        decode_symbol.append(qpsk[i])
    return np.asarray(decode_symbol)

def Loop_Filter(data):
    
    BnTs = 0.01 
    Nsps = 10
    C = np.sqrt(2)
    Kp = 1
    teta = ((BnTs)/(Nsps))/(C + 1/4*C)
    K1 = (-4*C*teta)/((1+2*C*teta+teta**2)*Kp)
    K2 = (-4*teta**2)/((1+2*C*teta+teta**2)*Kp)
    real = (data.real[0] - data.real[10+0]) * data.real[10//2+0]
    imag = (data.imag[0] - data.imag[10+0]) * data.imag[10//2+0]
    error = real + imag 
    filter = (error.real * K1) + (error.real * K2)
    fil = filter/10
    return fil

    


data = sp.loadmat('C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\Lesson17\\recdata1702_5.mat')

h = list(data.values())
data = np.asarray(h[3])
data = np.ravel(data[:20000])

plt.figure(1)
plt.title("QPSK from file matlab")
plt.scatter(data.real, data.imag)

h1 = np.ones(10)
data = np.convolve(h1,data,"full")


n = np.arange(0,20)
plt.figure(2)
plt.title("Gardner TED")
plt.xlabel("tau")
plt.ylabel("e(ns)")
#plt.axvline(x=0,'r')
#for simbol in range(0,5):
    #err= TED(data,simbol)
    
    #plt.plot(err.real)
err= TED(data)
plt.plot(err.real)
print(err)

print(Loop_Filter(data))

data = Get_Index(data,2)
plt.figure(3)
plt.title("QPSK sync")

plt.scatter(data.real, data.imag)
#print(len(err))
plt.show()