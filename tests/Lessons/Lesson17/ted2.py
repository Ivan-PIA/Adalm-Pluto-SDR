import scipy. io as sp
from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM, text_from_bits, text_to_bits
import matplotlib.pyplot as plt
import numpy as np
import math



def TED(data): # for plot TED
    err = np.zeros(len(data)//10, dtype = "complex_")
    ted_plot = np.zeros(20, dtype = "complex_")
    #data = np.roll(data,-2)
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

def TED1(data): #original ted
    err = np.zeros(len(data)//10, dtype = "complex_")
    #data = np.roll(data,-2)
    nsp = 10
    
    for ns in range(0,len(data)-(2*nsp+9),nsp):
        real = (data.real[ns] - data.real[nsp+ns]) * data.real[nsp//2+ns]
        imag = (data.imag[ns] - data.imag[nsp+ns]) * data.imag[nsp//2+ns]
        err[ns//nsp] = real + imag 


    return err

def TED_loop_filter(data): #ted loop filter 
    BnTs = 0.01 
    Nsps = 10
    C = np.sqrt(2)/2
    Kp = 1
    teta = ((BnTs)/(Nsps))/(C + 1/(4*C))
    K1 = (-4*C*teta)/((1+2*C*teta+teta**2)*Kp)
    K2 = (-4*teta**2)/((1+2*C*teta+teta**2)*Kp)
    print("K1 = ", K1)
    print("K2 = ", K2)
    #K1_2 = (1/Kp)*((((4*C)/(Nsps**2))*((BnTs/(C + (1/4*C)))**2))/(1 + ((2 * C)/Nsps)*(BnTs/(C + (1/(4*C))))+(BnTs/(Nsps*(C+(1/4*C))))**2))
    err = np.zeros(len(data)//10, dtype = "complex_")
    data = np.roll(data,-0)
    nsp = 10
    p1 = 0
    p2 = 0
    n = 0
    mass_cool_inex = []
    mass_id = []
    for ns in range(0,len(data)-(2*nsp),nsp):
        #real = (data.real[ns+n] - data.real[nsp+ns+n]) * data.real[n+(nsp)//2+ns]
        #imag = (data.imag[ns+n] - data.imag[nsp+ns+n]) * data.imag[n+(nsp)//2+ns]
        real = (data.real[nsp+ns+n] - data.real[ns+n]) * data.real[n + (nsp)//2+ns]
        imag = (data.imag[nsp+ns+n] - data.imag[ns+n] ) * data.imag[n + (nsp)//2+ns]
        err[ns//nsp] = real + imag
        error = err.real[ns//nsp]
        p1 = error * K1
        p2 = p2 + p1 + error * K2
        #print(ns ," p2 = ",p2)  
        while(p2 > 1):
            #print(ns ," p2 = ",p2)
            p2 = p2 - 1
        #while(p2 < -1):
            #print(ns ," p2 = ",p2)
            #p2 = p2 + 1
        
        n = round(p2*10)  
        n1 = n+ns+nsp   
        mass_cool_inex.append(n1)
        mass_id.append(n)

    #mass_cool_inex = [math.ceil(mass_cool_inex[i]) for i in range(len(mass_cool_inex))]
    mass1 = np.asarray(mass_cool_inex)
    mass = np.asarray(mass_id)
    plt.subplot(2,1,1)
    plt.plot(err) 
    plt.subplot(2,1,2)
    plt.plot(mass)   
    
    return mass1


def Get_Index(qpsk, index): # вычленяет семпл выбранный глазковой диаграммой 
    decode_symbol = []
    for i in range(index,len(qpsk),10):
        #print()
        decode_symbol.append(qpsk[i])
    return np.asarray(decode_symbol)

 
def Get_Cool_Index(mass_index,qpsk):
    decode_symbol = []
    
    ns = 10 
    for i in range(0,len(qpsk)-40,10):
        decode_symbol.append(qpsk[mass_index[i//ns] + i])
    return np.asarray(decode_symbol)


def PLL(conv):
    mu = 0  # коэфф фильтра 
    theta = 1 # начальная фаза
    phase_error = np.zeros(len(conv))  # фазовая ошибка
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        theta_hat = np.angle(conv[n])  # оценка фазы
        #print(theta_hat)
        phase_error[n] = theta_hat - theta  # фазовая ошибка
        output_signal[n] = conv[n] * np.exp(-1j * theta)  # выходной сигнал
        theta = theta + mu * phase_error[n]  # обновление
    return output_signal

data = sp.loadmat('C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\Lesson17\\recdata1702_5.mat')

h = list(data.values())
data = np.asarray(h[3])
data = np.ravel(data[0:40000])

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

err= TED(data)
plt.plot(err.real)
#print(err)
plt.figure(3)
data = PLL(data)
#### для p2
#TED_loop_filter(data)

mass_index = TED_loop_filter(data)
index_mean = np.mean(mass_index)
print(index_mean)
#plt.plot(mass_index)
#print("mean for mass index = ", np.mean(mass_index))
#dec = np.full(len(data/10),2)

new_data = data[mass_index]
print(len(new_data))
#new_data = np.asarray(new_data)
#data = Get_Cool_Index(mass_index , data)
#data = Get_Cool_Index(dec , data)
plt.figure(4)
plt.title("QPSK sync")
Ns = len(mass_index)
nn_start = round(Ns / 5)
nn_end = Ns - round(Ns / 5)
nn = np.arange(nn_start, nn_end)

plt.scatter(new_data[700:].real, new_data[700:].imag)


plt.show()