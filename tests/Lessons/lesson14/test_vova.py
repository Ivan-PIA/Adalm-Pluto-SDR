import numpy as np
import matplotlib.pyplot as plt
# Ссылка: https://nicoskin.notion.site/LO-0b7202cc15e7451e8590d45c7b3b1f0b
 
t = np.arange(0, 1, 1/10000) # Частота дискретизации 10000 - якобы аналоговый сигнал
x = np.cos(2*np.pi*t*5) + np.sin(2*np.pi*t*15)
i = np.cos(2*np.pi*t*1000) * x
q = np.sin(2*np.pi*t*1000) * x
 
t = np.arange(0, 1, 1/200) # Частота дискретизации 200
x = (np.cos(2*np.pi*t*5) + np.sin(2*np.pi*t*15))
i = np.cos(2*np.pi*t*1001) * x
q = np.sin(2*np.pi*t*1001) * x
 
# scatter чтобы увидеть как смещается фаза
plt.figure(1)
stop_t = 60
plt.axhline(0,color='r')
plt.axvline(0,color='r')
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.scatter(i[:stop_t],q[:stop_t])
plt.plot(i[:stop_t],q[:stop_t])
i2 = np.cos(2*np.pi*t*1000) * x
q2 = np.sin(2*np.pi*t*1000) * x
plt.scatter(i2[:stop_t],q2[:stop_t])
plt.plot(i2[:stop_t],q2[:stop_t])
 
 
 
plt.figure(2)
plt.stem(i)
plt.plot(x, 'r')
plt.show()