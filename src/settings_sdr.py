import adi
import numpy as np


def standart_settings(Pluto_IP = "192.168.2.1", sample_rate = 1e6, buffer_size = 1e3, gain_mode = 'manual'):
    sdr = adi.Pluto(Pluto_IP)
    sdr.sample_rate = int(sample_rate)
    sdr.rx_buffer_size = int(buffer_size)
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
    sdr.gain_control_mode_chan0 = gain_mode
    return sdr


def rx_signal(sdr, rx_lo, gain_rx, cycle):
    sdr.rx_lo = int(rx_lo)
    sdr.rx_hardwaregain_chan0 = gain_rx
    data = np.zeros(0)
    for i in range(cycle):
        rx = sdr.rx()
        data = np.concatenate([data,rx])
    sdr.tx_destroy_buffer()
    return data
    
    
    

def tx_signal(sdr, tx_lo, gain_tx, data, tx_cycle: bool = True):
    sdr.tx_lo = int(tx_lo)
    sdr.tx_hardwaregain_chan0 = gain_tx
    sdr.tx_cyclic_buffer = tx_cycle
    sdr.tx(data)