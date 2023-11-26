import adi
import matplotlib.pyplot as plt
#import pylab as plt
import matplotlib.animation as animation

sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def DrawData(e):
    rx_data = sdr.rx()


    x_real_data = []
    y_imag_data = []
    time_data = []


    i2 = 1
    for i in rx_data:
        
        x_real_data.append(i.real)
        y_imag_data.append(i.imag)
        time_data.append(i2)
        i2+=1
    ax1.clear()
    plt.plot(time_data, x_real_data, c = 'g')
    plt.plot(time_data, y_imag_data, c = 'r')



ani = animation.FuncAnimation(fig, DrawData, interval=100)
    
plt.show()


