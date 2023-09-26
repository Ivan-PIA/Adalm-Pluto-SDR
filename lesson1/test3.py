import adi
#import matplotlib.pyplot as plt
import pylab as plt

sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR
sdr.sample_rate = int(2.5e6)
rx_data = sdr.rx()

x_real_data = []
y_imag_data = []
time_data = []

print(type(sdr))
print("rx data length: ",len(rx_data))
i2 = 1
for i in rx_data:
    
    x_real_data.append(i.real)
    y_imag_data.append(i.imag)
    time_data.append(i2)
    
    i2+=1

#plt = plt.subplot(111)
#plt.scatter(x_real_data, y_imag_data)
#plt.subplot (1, 2, 1)
plt.plot(time_data, x_real_data, c = 'g', )#, marker='x', label='1')
plt.title("Real data")
#plt.subplot (1, 2, 2)

plt.plot(time_data, y_imag_data, c = 'r')#, marker='s', label='-1' )
#plt.plot(x_real_data, y_imag_data, )
#plt.legend("Test")
plt.title("Img data")
plt.show()


