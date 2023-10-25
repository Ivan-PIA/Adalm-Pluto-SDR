import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import kaiserord, lfilter, firwin, freqz
from scipy import fftpack
 
 
t=np.arange(0,1,0.01)
cs=np.cos(2*np.pi*10*t)
ss=np.sin(2*np.pi*10*t)
I=-3
Q=-1
S2=I*cs
S3=Q*ss
 
plt.figure(1)
plt.plot(t,S2)
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Косинус')
 
plt.figure(2)
plt.plot(t,S3)
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Синус')
 
qam=S2+S3
 
plt.figure(3)
plt.plot(qam) # символ КАМ модулированного сигнала
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Cимвол КАМ сигнала')


qam2=qam**2 # формирование нормального щума с мошностью, нужной для заданного ОСШ
qam_db=10*np.log10(qam2)
snr_db=4 # требуемое ОСШ в ДБ
sig_awg_watts=np.mean(qam2)
sig_awg_db=10*np.log10(sig_awg_watts)
noise_awg_db=sig_awg_db - snr_db
noise_awg_watts=10**(noise_awg_db/10)
mean_noise=0
noise_volts=np.random.normal(mean_noise, np.sqrt(noise_awg_watts),len(qam2))
 
plt.figure(4)
plt.plot(noise_volts)
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Реализация шума')

qam_n=qam+noise_volts

plt.figure(5)
plt.plot(qam_n) # символ КАМ модулированного сигнала с шумом
plt.figure(6)
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Cимвол КАМ сигнала с шумом')

XK=np.fft.fft(qam)
K=np.arange(100)
plt.plot(K,np.abs(XK))  # модуль спектра КАМ модулированного сигнала
plt.xlabel('частота ДПФ')
plt.ylabel('Амплитуда символа')
plt.title('спектр КАМ сигнала')
 
p1=np.cos(2*np.pi*10*t) #   опорный косинус в приемнике
p2=np.sin(2*np.pi*10*t)  # опорный синус в приемнике
rc=qam*p1 # умножаем принятый сигнал на опорный косинус
rs=qam*p2 # умножаем принятый сигнал на опорный синус
 
plt.figure(7)
 
XK=np.fft.fft(rc) 
K=np.arange(100)
plt.plot(K,np.abs(XK)) # модуль спектра символа после умножения на опорный косинус в приемнике
plt.xlabel('частота ДПФ')
plt.ylabel('Амплитуда символа')
plt.title('  модуль спектра символа после умножения на опорный косинус')

 
n=61
taps=signal.firwin(n,0.1) #  вычисляем импульсную характеристику цифрового ФНЧ
plt.plot(taps)
plt.show()
w,h=signal.freqz(taps,worN=8000) # частотная характеристика фнч
rcf=2*signal.lfilter(taps,1.0,rc) #  фильтрация в фнч косинусной части принятого сигнала
plt.figure(8)
plt.plot(rcf)
plt.figure(9)
rsf=2*signal.lfilter(taps,1.0,rs) #  фильтрация в фнч  синусной части принятого сигнала
plt.plot(rsf)
plt.xlabel('Длительность символа [с]')
plt.ylabel('Амплитуда символа')
plt.title('Cигнал на выходе фильтра')


 


