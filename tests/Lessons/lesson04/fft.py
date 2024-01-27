from scipy.fftpack import fft, ifft,  fftshift
import numpy as np
import matplotlib.pyplot as plt


fc=100 # Частота косинуса 
fs=32*fc # частота дискретизации, избыточная 
t=np.arange( 0, 2,  1/fs) # длительность сигнала 2 с
x=np.cos(2*np.pi*fc*t) # формирование временного сигнала


plt.figure(1)
plt.stem(t,x)
#выбрать длительность 0.2 сек
plt.xlabel( '$ t=nT_s$ ' )
plt.ylabel( '$x [ n ] $ ' )

#Далее вычисляется ДПФ длиной N = 256 точек в интервале частот 0 − fs.
N=256 # количество точек ДПФ
X=fft(x,N)/N

k2 = np.arange(-N/2, N/2)
df=fs/N
kf2=k2*df
X2 = fftshift(X) # сдвиг ДПФ на центр
plt.figure(4)
plt.stem(kf2,abs(X))
plt.xlabel('Гц' )
plt.ylabel( '$x [ k ] $' )

plt.show()