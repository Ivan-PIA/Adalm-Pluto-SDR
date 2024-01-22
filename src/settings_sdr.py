import adi



def standart_settings(Pluto_IP = "192.168.2.1", sample_rate = 1e6, buffer_size = 1e3):
    sdr = adi.Pluto(Pluto_IP)
    sdr.sample_rate = sample_rate
    sdr.buffer_size = buffer_size
    return sdr


def init_rx(sdr, rx_lo, gain_rx):
    sdr.rx_lo = rx_lo
    sdr.rx_hardwaregain_chan0 = gain_rx
    
    
    

def init_tx(sdr, rx_lo, gain_tx):
    sdr.rx_lo = rx_lo
    sdr.rx_hardwaregain_chan0 = gain_tx