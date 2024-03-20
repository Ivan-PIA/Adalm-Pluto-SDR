from scipy.fftpack import fft, ifft, fftshift
import numpy as np
import matplotlib.pyplot as plt


T=10**-4 # Длительность символа
Nc=16 # Количество поднесущих
df=1/T # Частотный интервал между поднесущими
ts=T/Nc # Интервал дискретизации
k=3
t= ts * np.arange(0,Nc) 

s =  1/np.sqrt (T) * np.exp(1j * 2 * np.pi * k * df * t ) # Формирование одной поднесущей с частотой f ∗ df

plt.figure(1)
plt.plot(t, s.real ) #реальная часть поднесущей

sc_matr = np.zeros((Nc, len(t)) , dtype=complex)
sd = np.zeros ( ( 1 , Nc ) , dtype=complex)#передоваемые данные

# Матрица из поднесуших
for k in range (Nc):
    sk_k= 1/np.sqrt(T) * np.exp(1j *2*np . pi * k * df * t )

    sc_matr [k,: ] = sk_k

#sd − вектор Nc передаваемых комплексных символов
    
sd = np.sign(np.random.rand(1,Nc) - 0.5) + 1j * np.sign(np.random.rand(1, Nc) - 0.5)

sd= sd.reshape(Nc)

print(sd)

xt=np.zeros((1, len(t)), dtype=complex)

# формирование суммы модулированных поднесущих

for k in range (Nc):
    sc = sc_matr [k, : ]
    xt = xt + sd[k] * sc

xt=xt.reshape(Nc) 

# реальная часть сформированного OFDM символа

plt.figure(2)
plt.plot(t, xt.real)

#формирование OFDM символа при помощи ОДПФ

xt2 = np.fft.ifft(sd , 16) 

# реальная часть сформированного OFDM символа

plt.figure( 3 )
plt.plot(t , xt2.real )
n=3

#прием символа на n поднесущей в виде интеграла отпроизведения принятого символа на опорное колебание на nподнесущей

sr= ts * np.sum(xt * np.conjugate(sc_matr[n , : ]) ) 
#прием символа на Nc поднесущих при помощи ДПФ принятого символа

sr2=np.sqrt(T) /Nc * np.fft.fft(xt)

#plt.figure( 4 )
#print(sr2)
print("rx : ",sd[3])
print("tx : ",sr)

print(sr2[3])




plt.show()