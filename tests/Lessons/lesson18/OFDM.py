import matplotlib.pyplot as plt
import numpy as np

T = 10**(-4)

Nc = 4
df = 10**4
fs = 4*df
ts = 1/fs

t = np.arange(0,T,0.1*ts)
s = np.array([1+1j, 2 + 5j, -1 + 5j, 3+ 4j]) 
f1 = 1 * df
f2 = 2 * df
f3 = 3 * df
f4 = 4 * df

xt = np.zeros(len(t),dtype = "complex_")
xt2 = np.zeros(len(t),dtype = "complex_")
xt3 = np.zeros(len(t),dtype = "complex_")
xt4 = np.zeros(len(t),dtype = "complex_")
xtitog = np.zeros(len(t),dtype = "complex_")
for i in range(len(t)):

    xt[i] = s[0] * np.exp(1j*2*np.pi*0*t[i])
    xt2[i] = s[1] * np.exp(1j*2*np.pi*f1*t[i])
    xt3[i] = s[2] * np.exp(1j*2*np.pi*f2*t[i])
    xt4[i] = s[3] * np.exp(1j*2*np.pi*f3*t[i])

ofdm = xt + xt2 + xt3 + xt4   
deofdm = ofdm *xt2 # получаем умножение
integr = (np.sum(deofdm*ts*0.1))/np.sqrt(T)

print(integr)
plt.figure(1)
plt.plot(xt.real)
plt.plot(xt2.real)
plt.plot(xt3.real)
plt.plot(xt4.real)

plt.figure(2)
plt.plot(deofdm.real)
#plt.plot(xtitog1.imag)
plt.show()
print(len(t))