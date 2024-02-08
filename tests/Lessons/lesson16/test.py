import matplotlib.pyplot as plt
import numpy as np
from context import *
import adi

sdr = standart_settings()

init_rx(sdr,2e9,-5)