from scipy.fftpack import fft, ifft,  fftshift
import numpy as np
import matplotlib.pyplot as plt


fc=10 # Частота косинуса 
fs=32*fc # частота дискретизации, избыточная 
t=np.arange( 0, 2,  1/fs) # длительность сигнала 2 с
x=np.cos(2*np.pi*fc*t) # формирование временного сигнала


fc1=10*2 # Частота косинуса 
fs1=32*fc1
t1=np.arange( 0, 2,  1/fs1) 
x1=np.cos(2*np.pi*fc1*t1) 

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(t,x) 
plt.subplot(2,1,2)
plt.plot(t1,x1)
plt.show()
# plt.subplot(2,1,2)
# plt.stem(t,x) # для отображения временных отсчетов сигнала, выбрать длительность 0.2 сек



# plt.xlabel('$t=nT_s$')
# plt.ylabel('$x[n]$') 
# N=256 # количество точек ДПФ
# X = fft(x,N)/N # вычисление ДПФ и нормирование на N
# plt.figure(2)
# k = np.arange(0, N)
# plt.stem(k,abs(X)) # выводим модуль ДПФ 

# k2 = np.arange(-N/2, N/2)
# X2 = fftshift(X) # сдвиг ДПФ на центр 
# plt.figure(3)
# plt.stem(k2,abs(X2))