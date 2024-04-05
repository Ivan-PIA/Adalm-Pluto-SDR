from context import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft,  fftshift, ifftshift

bit = text_to_bits('kadsbkabfjakhcbajdcjkhkdkjnjsdnnb cdjk')


qpsk = QPSK(bit)
nc = len(qpsk)
noise = np.random.normal(0,100,len(qpsk)) + 1j * np.random.normal(0,100,len(qpsk))


plot_QAM(qpsk, title= "qpsk" )
plt.figure(2)
plt.title("ifft")
ofdm = ifft(qpsk,nc)
ofdm += noise
plt.plot(ofdm)
noise = np.random.normal(0,1,len(ofdm))
ofdm = ofdm + noise

print(ofdm)

deqpsk = fft(ofdm,nc)

plot_QAM(deqpsk, title= "qpsk" )

deqpsk = DeQPSK(deqpsk)

text = bits_array_to_text(deqpsk)
print(text)
plt.show()