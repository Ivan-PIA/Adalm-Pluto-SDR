from context import printt
from context import plot
import numpy as np
printt()

a = np.arange(-10,10,0.01)
b = np.cos(10*a)

plot(a,b)