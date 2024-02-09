from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt
import numpy as np

bit = randomDataGenerator(1000)

#plot_QAM(QPSK)


def eye_diagram(qpsk):
    q = qpsk
    print(qpsk.real)
    for i in range(0,len(qpsk),10):
        plt.plot(q.real[0:10])
        q = np.roll(qpsk,-10)
        qpsk = q
    

def On_eye_dig(qpsk, index): # вычленяет семпл выбранный глазковой диаграммой 
    decode_symbol = []
    for i in range(index,len(qpsk),10):
        #print()
        decode_symbol.append(qpsk[i])
    return np.asarray(decode_symbol)


h1 = np.ones(10)
QPSK = QPSK(bit)
QPSK = np.repeat(QPSK, 10)
conv = np.convolve(h1,QPSK,'same')
noise = np.random.normal(0,0.1,len(conv))
conv= conv+noise
#QPSK = QPSK + noise_qpsk
#noise_qpsk = np.random.normal(0,0.1,len(QPSK))

plt.figure(1)
plt.scatter(QPSK.real, QPSK.imag)
plt.figure(2)

eye_diagram(conv)
plt.figure(3)

plt.figure(4)
decode = On_eye_dig(conv,5)
plt.scatter(decode.real, decode.imag)

plt.show()
