# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 16:12:43 2023

@author: alex
"""

from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt


fc=10 # Частота косинуса 
fs=32*fc # частота дискретизации, избыточная 
t=np.arange( 0, 2,  1/fs) # длительность сигнала 2 с
x=np.cos(2*np.pi*fc*t) # формирование временного сигнала
plt.figure(1)
plt.plot(t,x) 
#plt.stem(t,x) # для отображения временных отсчетов сигнала, выбрать длительность 0.2 сек
plt.xlabel('$t=nT_s$')
plt.ylabel('$x[n]$') 
N=256 # количество точек ДПФ
X = fft(x,N)/N # вычисление ДПФ и нормирование на N
plt.figure(2)
k = np.arange(0, N)
plt.stem(k,abs(X)) # выводим модуль ДПФ в точках ДПФ
plt.xlabel('k')
plt.ylabel('$x[k]$') 

df=fs/N
kf = k*df
plt.figure(3)
plt.stem(kf,abs(X)) # выводим модуль ДПФ в частотах 
plt.xlabel('Гц')
plt.ylabel('$x[k]$') 


k2 = np.arange(-N/2, N/2)
kf2=k2*df
X2 = fftshift(X) # сдвиг ДПФ на центр 
plt.figure(4)
plt.stem(kf2,abs(X2))
plt.xlabel('Гц')
plt.ylabel('$x[k]$') 


plt.figure(5)
x_ifft = N*ifft(X,N)
t = np.arange(0, len(x_ifft))/fs
plt.plot(t ,np.real(x_ifft ))
#plt.stem(t ,np.real(x_ifft )) # временные отсчеты колебания
plt.xlabel('c')
plt.ylabel('$x[n]$') 
plt.show()
