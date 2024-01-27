import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import max_len_seq

way = 'lesson11\qpsk_iq.csv'
data_rx = np.loadtxt(way, dtype=np.complex64, delimiter=",")

def first():
    plt.figure(1)

    plt.axhline(color='r', linestyle = '--')
    plt.axvline(color='r',linestyle = '--')
    plt.scatter(data_rx.real,data_rx.imag)


    plt.figure(2)
    plt.axhline(color='r',linestyle = '--')
    plt.axvline(color='r', linestyle = '--')
    plt.xlim(-3000,3000)
    plt.ylim(-3000,3000)

    xrec = data_rx/np.mean(data_rx**2)

    plt.scatter(xrec.real, xrec.imag)



first()
plt.show()



