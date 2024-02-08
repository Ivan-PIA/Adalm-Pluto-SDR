from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt
import numpy as np

bit = randomDataGenerator(100)




#plot_QAM(QPSK)


def eye_diagram(qpsk):
    q = qpsk
    print(qpsk.real)
    for i in range(0,len(qpsk),20):
        
        plt.plot(q.real[0:20])
        q = np.roll(qpsk,-20)
        qpsk = q
    plt.show()


def eye_diagram1(qpsk):
    #t = np.zeros(len(qpsk))
    for i in range(len(qpsk)):
        #print(len(qpsk))
        #print(np.roll(qpsk.real,-10))
        plt.plot(np.roll(qpsk.real[i:i+3],3))
    plt.show()

def eye_diagram_var2(qpsk):
    qpsk = np.reshape(qpsk,10)
    plt.plot(qpsk)
    plt.show()




h1 = np.ones(10)
QPSK = QPSK(bit)
QPSK = np.repeat(QPSK, 10)
conv = np.convolve(h1,QPSK)
noise = np.random.normal(0,0.5,len(conv))
noise_qpsk = np.random.normal(0,0.1,len(QPSK))
conv= conv+noise
QPSK = QPSK + noise_qpsk

eye_diagram(conv)
#plt.plot(QPSK.real)
#plt.show()