import adi
import matplotlib.pyplot as plt

sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR
sdr.sample_rate = int(2.5e6)
rx_data = sdr.rx()
x_real_data = []
y_imag_data = []
print("rx data length: ",len(rx_data))
for i in rx_data:
    x_real_data.append(i.real)
    y_imag_data.append(i.imag)

plt.scatter(x_real_data, y_imag_data )
plt.show()