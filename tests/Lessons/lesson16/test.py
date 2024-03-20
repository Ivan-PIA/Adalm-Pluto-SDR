import matplotlib.pyplot as plt
import numpy as np
from context import *
import adi

sdr = standart_settings("ip:192.168.3.1", 1e6, 1e3)

#rx_signal(sdr,2e9,20)
#tx_signal(sdr,2e9,0)


bit = text_to_bits("lalalavavavavavfjkafbaldjgvbcljbphlskjlskkck,dnkhehdvbh")

barker = np.array([1,1,0,1,0,1,1,0,0,1,1,0,0])
barker_2 = np.repeat(barker,2)
bit_sinc = np.concatenate([barker_2,bit])

qpsk1 = QPSK(bit_sinc)
qpsk_symbol = np.repeat(qpsk1,10)

plt.figure(1)
plt.scatter(qpsk_symbol.real,qpsk_symbol.imag)

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


def PLL(conv):
    mu = 1# коэфф фильтра 
    theta = 0 # начальная фаза
    phase_error = np.zeros(len(conv))  # фазовая ошибка
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        theta_hat = np.angle(conv[n])  # оценка фазы
        #print(theta_hat)
        phase_error[n] = theta_hat - theta  # фазовая ошибка
        output_signal[n] = conv[n] * np.exp(-1j * theta)  # выходной сигнал
        theta = theta + mu * phase_error[n]  # обновление
    return output_signal



def dpll(reference_signal, input_signal, phase_error=0, frequency_error=0):
    PHASE_ERROR_GAIN = 0.1
    FREQUENCY_ERROR_GAIN = 0.01
    phase_error = phase_error
    frequency_error = frequency_error

    filtered_input_signal = np.zeros_like(input_signal)

    for i in range(1, len(input_signal)):
        # Рассчитываем фазовую и частотную ошибки
        phase_error += PHASE_ERROR_GAIN * (reference_signal[i] - input_signal[i])
        frequency_error += FREQUENCY_ERROR_GAIN * phase_error

        # Корректируем фазу входного сигнала
        freq = 2 * np.pi * frequency_error
        phase_increment = np.exp(1j * freq)
        filtered_input_signal[i] = input_signal[i] * phase_increment

    return filtered_input_signal
 
tx_signal(sdr,2e9,0,qpsk_symbol)

rx = rx_signal(sdr,2e9,20,40)


rxMax = max(rx.real)
rx = rx / rxMax

plt.figure(4)
plt.scatter(rx.real,rx.imag)


h1 = np.ones(10)
data = np.convolve(h1,rx,"full")/10

plt.figure(2)
ted_ind = TED_loop_filter(data)

data = data[ted_ind]
data =  PLL(data)


plt.figure(3)
plt.scatter(data[1000:].real,data[1000:].imag)

# def Correlat(gold, signal):
#     max = 0
#     for j in range(len(signal)-len(gold)):
#         corr_sum = np.correlate(gold, signal[:(len(gold))])
#         if corr_sum > max:
#             max = corr_sum
#             index = j
#         signal = np.roll(signal,-1)
#     return index

# ind = Correlat(barker_2,data)
# print(ind)
# data_sinc = data[ind:]
# data_sinc = data[:len(bit)]

# deqpsk = DeQPSK(data_sinc)

# bit = list(map(int,deqpsk))

# #bit = "".join(map(str, bit))

# #decode_name = text_from_bits(bit)
# #print(decode_name)

plt.show()

