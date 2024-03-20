from context import QPSK, text_to_bits
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft,  fftshift, ifftshift

bit = text_to_bits('kadsbkabfjakhcbajdcjkhkdkjnjsdnnb cdjk')

nc = 16
qpsk = QPSK(bit)
plt.figure(1)
plt.scatter(qpsk.real,qpsk.imag)
plt.figure(2)
ofdm = ifft(qpsk,16)
plt.plot(ofdm)
noise = np.random.normal(0,1,len(ofdm))
ofdm = ofdm + noise

print(ofdm)

deqpsk = fft(ofdm,16)
plt.figure(3)
plt.scatter(deqpsk.real,deqpsk.imag)
plt.show()