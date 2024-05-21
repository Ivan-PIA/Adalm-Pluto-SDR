import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2.5, 250)
f = np.exp(2*np.pi*2*1j*t)
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')
ax.grid()
x=f.real
y=f.imag
ax.plot3D(t, x, y,'r')
ax.set_title('Комплексная экспонента')
ax.plot3D(t, x,np.zeros(250),'b')
ax.plot3D(t,np.zeros(250),y,'g')
 
ax.set_xlabel('Time')
ax.set_ylabel('Real Axis')
ax.set_zlabel('Imag Axis')
plt.show()