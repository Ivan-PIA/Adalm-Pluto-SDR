from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt


fc=10
fc1=100 # Частота косинуса 
fs=320 # частота дискретизации, избыточная 
t=np.arange( 0, 2,  1/fs) # длительность сигнала 2 с
x=np.cos(2*np.pi*fc*t)+2*np.cos(2*np.pi*fc1*t) # формирование временного сигнала
plt.figure(1)
plt.plot(t,x) 
#plt.stem(t,x) # для отображения временных отсчетов сигнала, выбрать длительность 0.2 сек
plt.xlabel('$t=nT_s$')
plt.ylabel('$x[n]$') 
N=512 # количество точек ДПФ
X = fft(x,N)/N # вычисление ДПФ и нормирование на N


# # #plt.figure(2)
# k = np.arange(0, N)
# # #plt.stem(k,abs(X)) # выводим модуль ДПФ в точках ДПФ
# # #lt.xlabel('k')
# # plt.ylabel('$x[k]$') 

# df=fs/N
# kf = k*df
# plt.figure(2)
# plt.stem(kf,abs(X)) # выводим модуль ДПФ в частотах 
# plt.xlabel('Гц')
# plt.ylabel('$x[k]$') 



# k2 = np.arange(-N/2, N/2)
# kf2=k2*df
# X2 = fftshift(X) # сдвиг ДПФ на центр 
# #plt.figure(4)
# #plt.stem(kf2,abs(X2))
# #lt.xlabel('Гц')
# #lt.ylabel('$x[k]$') 


# #plt.figure(5)
# x_ifft = N*ifft(X,N)
# t = np.arange(0, len(x_ifft))/fs
# #plt.plot(t ,np.real(x_ifft ))
# #lt.stem(t ,np.real(x_ifft )) # временные отсчеты колебания
# #lt.xlabel('c')
# #lt.ylabel('$x[n]$') 

X = np.arrey([0,0,2-1j,0,0,0,0,0])

