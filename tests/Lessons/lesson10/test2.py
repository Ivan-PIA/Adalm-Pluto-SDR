import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import max_len_seq

a = np.array([1, 1, 1, -1, 1])
b = np.correlate(a,a,'full')
print(b)
#plt.plot(b)



def gen_sig():
    data=max_len_seq(6)[0]

    #Преобразование нулей и единиц последовательности в передаваемое сообщение 
    m=2*data-1
    Ft= 100e3
    fs = 600e3

    ns = fs/Ft
    ts1 =np.array([0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1])

    b = np.ones(int(ns)) #Коэффициенты фильтра интерполятора

    ts1t = 2*ts1-1

    x_IQ = np.hstack((ts1t,m))

    #x_IQ = m # формирование пакета 
    N_input = len(x_IQ)
    xup = np.hstack((x_IQ.reshape(N_input,1),np.zeros((N_input, int(ns-1)))))

    xup= xup.flatten()

    x1 = signal.lfilter(b, 1,xup)

    x=x1.astype(complex) # in complex

    xt=.5*(1+x) #комплексные отсчеты для adalm

    triq=2**14*xt # in format
    print(len(triq))
    
    return triq

data = gen_sig()

plt.plot(data)
plt.show()