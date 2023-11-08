import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft,  fftshift, ifftshift

A =1
f1=10
f2 =20
fs=100
T = 1/fs
N=256
t = np.linspace(0, (N-1)*T, N)
x = A * np.cos(2 * np.pi * f1 * t) + A * np.cos(2 * np.pi * f2 * t)



X = np.fft.fft(x)

freq = np.fft.fftfreq(N, d=T)



plt.stem(freq,np.abs(X))
plt.show()

