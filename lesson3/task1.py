#import matplotlib.pyplot as plt 
#import numpy as np

import adi

# Create radio
sdr = adi.Pluto("ip:192.168.2.1")
rx_data = sdr.rx()
print("len sdr.rx = ", len(rx_data))
print(rx_data)