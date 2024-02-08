import matplotlib.pyplot as plt
import numpy as np
from context import *
import adi

sdr = standart_settings()

init_rx(sdr,2e9,50)
init_tx(sdr,2e9,50)



