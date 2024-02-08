import adi



def standart_settings(Pluto_IP = "192.168.2.1", sample_rate = 1e6, buffer_size = 1e3, gain_mode = 'manual'):
    sdr = adi.Pluto(Pluto_IP)
    sdr.sample_rate = int(sample_rate)
    sdr.buffer_size = int(buffer_size)
    sdr.gain_control_mode_chan0 = gain_mode
    return sdr


def init_rx(sdr, rx_lo, gain_rx):
    sdr.rx_lo = int(rx_lo)
    sdr.rx_hardwaregain_chan0 = gain_rx
    
    
    

def init_tx(sdr, tx_lo, gain_tx):
    sdr.tx_lo = int(tx_lo)
    sdr.tx_hardwaregain_chan0 = gain_tx