import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft,  fftshift, ifftshift
from scipy import signal
from scipy.signal import kaiserord, lfilter, firwin, freqz

A =1
f1=10
f2 =20
fs=200
T = 1/fs
N=256
t = np.linspace(0, (N-1)*T, N)
x = A * np.cos(2 * np.pi * f1 * t) + A * np.cos(2 * np.pi * f2 * t)


X = np.fft.fft(x)
freq = np.fft.fftfreq(N, d=T)

n=N
fn =  f2/fs             # нормированная частота
taps=signal.firwin(n,fn) # вычисляем ИХ ФНЧ с нормированной частотой 
d=2*signal.lfilter(taps,1.0,x) # сигнал на выходе ФНЧ 
plt.figure(1)

plt.stem(taps)
plt.title('Импульсная характеристика ')
plt.xlabel('t')
plt.ylabel('m(t)') 


Xdd = fft(d)/N # вычисление ДПФ и нормирование на N
plt.figure(2)
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100]  ,abs(Xdd[0:100] )) 
plt.title('Спектр сигнала на выходе ФНЧ')
plt.xlabel('f, Hz')
plt.ylabel('m(f)')

plt.figure(3)
plt.stem(freq,np.abs(X))
plt.title('спектр ДПФ')
plt.xlabel('f, Hz')
plt.ylabel('m(f)')


plt.figure(4)
plt.plot(t,x)
plt.title('Сигнал из двух составляющих')
plt.xlabel('t, s')
plt.ylabel("Ampl")
plt.show()
