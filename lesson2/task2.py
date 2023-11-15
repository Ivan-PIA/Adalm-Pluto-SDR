import numpy as np
import random
import matplotlib.pyplot as plt




n = 40
# time vector
t = np.linspace(0, 1, n)
# sine wave
x = np.sin(np.pi*t) + np.sin(2*np.pi*t) + np.sin(3*np.pi*t) + np.sin(5*np.pi*t)+1 # генерация сигнала

fig = plt.figure(figsize=(16, 8), dpi=100)

plt.plot(t, x, 'g', label = 'Аналоговый')
plt.stem(t, x, 'y',label = 'Дискретный')
plt.step(t, x,'r', label = 'Квантованный')

plt.xlabel('Time, s')
plt.ylabel('Amplitude')
plt.grid(linewidth=0.5)
plt.legend(fontsize=15)
plt.show()
