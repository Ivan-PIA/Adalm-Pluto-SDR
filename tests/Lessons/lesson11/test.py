import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import max_len_seq
 

# sdr = adi.Pluto('ip:192.168.2.1')
# sdr.sample_rate = 1000000
# sdr.tx_destroy_buffer()
 

# sdr.rx_lo = 2300000000
# sdr.tx_lo = 2300000000
# sdr.tx_cyclic_buffer = True
# #sdr.tx_cyclic_buffer = False
# sdr.tx_hardwaregain_chan0 = -5
# sdr.gain_control_mode_chan0 = "slow_attack"


# fs = sdr.sample_rate

#формируем радио сигнал на отправку на TX

fs = 1e6
rs=100000
ns=fs//rs #10
 

data=max_len_seq(4)[0] 
data = np.concatenate((data,np.zeros(1)))
 
 
x_ = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])
b7=np.array([1,-1,1,1,1,-1,1])
ts1 =np.array([0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1])
ts2 =[0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,1,1,0,1,1,1]
ts3 =[1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1]
ts4 =[1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,1,0,0]
m=2*data-1
 
ts1t=b7
 

b = np.ones(int(ns))
 
x_IQ = np.hstack((ts1t,m))
 
#x_IQ  =  m #data transmit
N_input = len(x_IQ)
xup = np.hstack((x_IQ.reshape(N_input,1),np.zeros((N_input, int(ns-1))))) # matrix 

xup= xup.flatten() #в одну строку 


x1 = signal.lfilter(b, 1,xup)# "1" и 9 нулей на фильтр на выходе уже 10 "1" 

x=x1.astype(complex)
print(x)
xt=.5*(1+x)
print(xt)
xiq=2**14*xt

#xiq=2**14*x_bb
#trdata = np.hstack((ts1,xt)).astype(complex)
triq=2**14*xt
print(triq)
#n_frame= len(triq)

n_frame= len(xiq)
print(n_frame)

