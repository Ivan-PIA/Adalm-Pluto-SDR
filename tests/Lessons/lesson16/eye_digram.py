from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt
import numpy as np

bit = randomDataGenerator(100)




#plot_QAM(QPSK)

#def eye_diagram(qpsk):

def eye_diagram(qpsk):
    #t = np.zeros(len(qpsk))
    q = qpsk
    for i in range(len(qpsk)):
        #print(len(qpsk))
        #print(np.roll(qpsk[i*10:i*10+10].real,-10))
        
        plt.plot(q[0:3].real)
        q = np.roll(qpsk,-3)
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




#h1 = np.ones(10)

QPSK = QPSK(bit)
#QPSK = np.repeat(QPSK, 10)
#conv = np.convolve(QPSK,h1)
noise = np.random.normal(0,0.015,len(QPSK))
QPSK= QPSK+noise

eye_diagram(QPSK)
#plt.plot(QPSK.real)
#plt.show()