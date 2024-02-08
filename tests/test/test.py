from context import QAM256, QAM64, QAM16, QPSK, randomDataGenerator, plot_QAM
import matplotlib.pyplot as plt
import numpy as np

bit = randomDataGenerator(1000)




#plot_QAM(QPSK)

#def eye_diagram(qpsk):

def eye_diagram(qpsk):
    #t = np.zeros(len(qpsk))
    for i in range(len(qpsk)):
        plt.plot(np.roll(qpsk[i:i+3],3))
    plt.show()

h1 = np.ones(10)

QPSK = QPSK(bit)
QPSK = np.repeat(QPSK, 10)
conv = np.convolve(QPSK,h1)
noise = np.random.normal(0,0.015,len(QPSK))
QPSK= QPSK+noise

eye_diagram(QPSK)
#plt.plot(QPSK.real)
#plt.show()