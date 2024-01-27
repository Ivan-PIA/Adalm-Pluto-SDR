import numpy as np
import adi
import matplotlib.pyplot as plt
import time

sample_rate = 1e6 # Hz
center_freq = 2e9 # Hz

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = 1000 

start_time = time.time()
rx = []
for cycle in range(int(sample_rate/1000)):
    new_data = sdr.rx()
    rx.extend(new_data)
end_time = time.time()
print(end_time-start_time)