import adi



def standart_settings(Pluto_IP, sample_rate):
    sdr = adi.Pluto(Pluto_IP)
    sdr.sample_rate = sample_rate
    return sdr


def init_rx(Pluto_IP, sample_rate, rx_lo, hardwaregain):
    sdr = standart_settings(Pluto_IP, sample_rate)
    sdr.rx_lo = rx_lo
    sdr.rx_hardwaregain_chan0 = hardwaregain
    
    
    

def init_tx(Pluto_IP, sample_rate, rx_lo, hardwaregain):
    sdr = standart_settings(Pluto_IP, sample_rate)
    sdr.rx_lo = rx_lo
    sdr.rx_hardwaregain_chan0 = hardwaregain