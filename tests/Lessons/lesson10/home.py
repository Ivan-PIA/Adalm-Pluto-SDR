from scipy import signal
from scipy.signal import max_len_seq
import matplotlib.pyplot as plt
import numpy as np

Ft= 100e3
fs = 600e3
rs = fs/10
ns = fs/Ft
b = np.ones(int(ns))
ts1 =np.array([0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1])

data=max_len_seq(6)[0]

xrec1 =  np.loadtxt('C:\\Users\\User\\Desktop\\visual\\Adalm-Pluto-SDR\\lesson10\\data.csv', dtype=np.complex64, delimiter=",")

xrec1 = np.asarray(xrec1)

xrec = xrec1/np.mean(xrec1**2)

fsr=2*np.pi*rs/fs
b2,a2 = signal.butter(10,fsr)
y1 = signal.lfilter(b2,a2,xrec)
#y2=signal.decimate(y1,int(ns))
yf=np.convolve(np.abs(y1.real),b)
y2=signal.decimate(yf,int(ns))

y=np.correlate(y2, ts1,'full')
plt.figure(1)
plt.plot(np.abs(y))
plt.show()
ind = np.argmax(abs(y),axis=0)
yy=y2[ind:ind+len(data)]