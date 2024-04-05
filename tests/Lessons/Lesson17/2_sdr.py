import scipy. io as sp
from context import *
import matplotlib.pyplot as plt
import numpy as np

def PLL(conv):
    mu = 1  
    theta = 0
    phase_error = np.zeros(len(conv))  
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        theta_hat = np.angle(conv[n]) 
       #print(theta_hat)
        phase_error[n] = theta_hat - theta  
        output_signal[n] = conv[n] * np.exp(-1j * theta)  
        theta = theta + mu * phase_error[n]  
    return output_signal

def FLL(conv):
    mu = 0
    omega = 0.5 # TODO: нужно протестировать для разных сигналов, пока непонятно, работает ли этот коэффициент для всех QPSK-сигналов
    freq_error = np.zeros(len(conv))
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        angle_diff = np.angle(conv[n]) - np.angle(output_signal[n-1]) if n > 0 else 0
        freq_error[n] = angle_diff / (2 * np.pi)
        omega = omega + mu * freq_error[n]
        output_signal[n] = conv[n] * np.exp(-1j * omega)
    return output_signal

def TED_loop_filter(data): #ted loop filter 
    BnTs = 0.01 
    Nsps = 10
    C = np.sqrt(2)
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
        #real = (data.real[nsp+ns+n] - data.real[ns+n]) * data.real[n + (nsp)//2+ns]
        #imag = (data.imag[nsp+ns+n] - data.imag[ns+n] ) * data.imag[n + (nsp)//2+ns]
        #err[ns//nsp] = np.mean(real + imag)
        err[ns//nsp] = np.mean((np.conjugate(data[nsp+ns+n]) - np.conjugate(data[ns+n]))*(data[n + (nsp)//2+ns])) 
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
    plt.figure(figsize=(8, 8))
    plt.subplot(2,1,1)
    plt.title('TED')
    plt.plot(err)
    
    plt.xlabel("Samples")
    plt.ylabel("Error")
     
    plt.subplot(2,1,2)
    plt.plot(mass)  
    plt.title("Selected index")
    plt.xlabel("Samples")
    plt.ylabel("Index") 
    
    return mass1



barkerCode = [+1, +1, +1, +1, +1, -1, -1, +1, +1, -1, +1, -1, +1]


mes = "lalalavavavavavfjkafbaldj123456781lalalavavavavavfjkafbaldj12erwdgns" #2 ofdm 
mes2 = "A small sfsdfsdfsf"
bit = randomDataGenerator(2400)
bit1 = text_to_bits(mes)


qpsk1 = QPSK(bit)

signalRepeat = np.repeat(qpsk1, 10)

###
### Работа с SDR
###

sdr = standart_settings("ip:192.168.2.1", 1e6, 1e3)
sdr2 = standart_settings("ip:192.168.3.1", 1e6, 1e3)


tx_signal(sdr,1900e6,0,signalRepeat)
rx_sig = rx_signal(sdr2,1900e6,20,50)

rxMax = max(rx_sig.real)
rx_sig = rx_sig / rxMax

symbolLength = 10 
rxConvolve = np.convolve(rx_sig, np.ones(symbolLength)) / 10 # Свёртка




Ted_index = TED_loop_filter(rxConvolve)
print(Ted_index[:10])

### тут TED, Loop Filter 
### и мы определяем какой отсчёт брать


rxАfterTED = rxConvolve[Ted_index]
rxАfterTED = rxАfterTED[2000:]
print(rxАfterTED)

plot_QAM(rxАfterTED, title="rxАfterTED")
plt.xlabel("real")
plt.ylabel("imag")


rxАfterTED = PLL(rxАfterTED)
plot_QAM(rxАfterTED, title=" after PLL")
plt.xlabel("real")
plt.ylabel("imag")
rxАfterTED = FLL(rxАfterTED)


plot_QAM(rx_sig , title="Rx signal")
plt.xlabel("real")
plt.ylabel("imag")



plot_QAM(rxАfterTED, title="Финальная фазовая подстройка")
plt.xlabel("real")
plt.ylabel("imag")



plt.show()