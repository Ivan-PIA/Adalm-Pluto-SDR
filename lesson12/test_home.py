import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import max_len_seq
from scipy.fftpack import fft, ifft,  fftshift, ifftshift








way = 'lesson12\qpsk_iq.csv'
xrec1 = np.loadtxt(way, dtype=np.complex64, delimiter=",")
size = len(xrec1)

plt.figure(1)
plt.scatter(xrec1.real, xrec1.imag)

xrec = xrec1**4 # возведение в степень qpsk
k = np.arange(0, size)
xrec2 = fft(xrec,size)
xrec2 = fftshift(xrec2)

w = np.linspace(-np.pi,np.pi,size)

max_f = np.argmax(abs(xrec2))



print(max_f)
max_index = w[max_f]
print("max in 'w' = ",max_index)

xrec = xrec1/np.mean(xrec1**2)
ph = max_index/4
phlc = np.exp(-1j*ph)
qpsk_ph = xrec1 *phlc
plt.figure(2)
plt.stem(w,abs(xrec2))
plt.figure(3)
plt.scatter(qpsk_ph.real, qpsk_ph.imag)
plt.show()