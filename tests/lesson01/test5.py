import adi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import numpy as np

sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR
sdr.sample_rate = int(2.5e6)

sdr.tx_rf_bandwidth = int(2.5e6) # filter cutoff, just set it to the same as sample rate
sdr.tx_hardwaregain_chan0 = -20 # Increase to increase tx power, valid range is -90 to 0 dB# Start the transmitter

sdr.tx_cyclic_buffer = True # Enable cyclic buffers


def gen_sin(x):

    data = []
    
    i = 0
    while(i < x):
        data.append(float(math.sin(i))**14)
        i+=0.1
    return data

#print(gen_sin(1000))

#sdr.tx(gen_sin(1000))



num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols
samples = np.repeat(x_symbols, 1) # 16 samples per symbol (rectangular pulses)
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.tx(samples) # st


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
    plt.ylim(-1000, 1000)
    plt.plot(time_data, x_real_data, c = 'g', )
    plt.plot(time_data, y_imag_data, c = 'r')



ani = animation.FuncAnimation(fig, DrawData, interval=100)
    
plt.show()


