import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import kaiserord, lfilter, firwin, freqz
from scipy import fftpack
 
Ts1=0.5e-3
t = np.arange(-20, 41)*Ts1
s =  np.cos(100*t*(2*np.pi))


plt.figure(1)
plt.subplot(3,1,1)
plt.plot(t, s )
plt.subplot(3,1,2)
plt.stem(t, s )


Ts2=2e-3
fs2=1/Ts2
t = np.arange(-5, 11)*Ts2
s =  np.cos(100*t*(2*np.pi))
plt.subplot(3,1,3)
plt.stem(t, s )
plt.show()
#plt.figure(2)
#plt.magnitude_spectrum(s,Fs=fs2,sides='twosided')

plt.figure(2)
 

sp = fftpack.fft(s)
#freqs = fftpack.fftfreq(len(s)) * fs2 
freqs=np.arange(0,fs2,fs2/len(s))
#fig, ax = plt.subplots()
plt.stem(freqs, np.abs(sp))
plt.xlabel('Частота в герцах [Hz]')
plt.ylabel('Модуль спектра')
plt.show()