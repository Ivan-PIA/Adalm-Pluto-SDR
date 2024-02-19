from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt
import numpy as np

bit = randomDataGenerator(100)

#plot_QAM(QPSK)


def eye_diagram(qpsk):
    #qpsk = np.roll(qpsk,-2)
    q = qpsk
    #print(qpsk.real)
    
    for i in range(0,len(qpsk),10):
        plt.plot(q.real[0:20])
        q = np.roll(qpsk,-10)
        qpsk = q
    

def On_eye_dig(qpsk, index): # вычленяет семпл выбранный глазковой диаграммой 
    decode_symbol = []
    for i in range(index,len(qpsk),10):
        #print()
        decode_symbol.append(qpsk[i])
    return np.asarray(decode_symbol)

def PLL(conv):
    mu = 0  # коэфф фильтра 
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

def gardner_te_detector(symbol_seq, samples_per_symbol):
    te = np.zeros(len(symbol_seq), dtype=np.complex128)
    
    for i in range(len(symbol_seq)):
        if i < 2*samples_per_symbol:
           continue
        
        te[i] = symbol_seq[i-samples_per_symbol] * (symbol_seq[i] - symbol_seq[i-2*samples_per_symbol])
        
    return te

h1 = np.ones(10)

QPSK = QPSK(bit)
QPSK = np.repeat(QPSK, 10)
noise = np.random.normal(0,0.05,len(QPSK))
QPSK = QPSK + noise

conv = np.convolve(h1,QPSK,'full')


#conv= conv+
#QPSK = QPSK + noise_qpsk
#noise_qpsk = np.random.normal(0,0.1,len(QPSK))
def gard_ted(conv1):
    errr = []
    error = 0
    for k in range(10,len(conv1),10):
        #print(k)
        error = (conv1.real[k-10]-conv1.real[k])*conv1.real[k//2]
        conv1 = np.roll(conv1, -1)
        
        errr.append(error)  
    print(errr)
    #plt.scatter(np.asarray(errr))



plt.figure(1)
plt.scatter(QPSK.real, QPSK.imag)

plt.figure(2)
eye_diagram(conv)

plt.figure(3)
plt.plot(conv.real)

#plt.figure(4)
conv1 = On_eye_dig(conv,9)
#plt.scatter(conv.real, conv.imag)


output_signal = PLL(conv)
plt.figure(5)
plt.scatter(output_signal.real,output_signal.imag)


#plt.figure(6)
#phase_error = PLL(conv)
#plt.plot(phase_error)


#print(te)

 
#conv1 = np.roll(conv,-5)

plt.show()