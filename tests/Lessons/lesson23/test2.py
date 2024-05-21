import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Создаем комплексный массив данных
x = np.array([1, 2, 3, 4, 5])
y = np.array([1+2j, -3+4j, 5+6j, -7+8j, 9+10j])

# Фильтруем отрицательные значения
mask = np.real(y) >= 0
x_filtered = x[mask]
y_filtered = y[mask]

# Разделяем вещественную и мнимую части
x_real = np.real(y_filtered)
x_imag = np.imag(y_filtered)

# Создаем функции интерполяции для вещественной и мнимой частей
f_real = interp1d(x_filtered, x_real, kind='cubic')
f_imag = interp1d(x_filtered, x_imag, kind='cubic')

# Создаем новый массив данных с пятью раз большим количеством точек
new_x = np.linspace(x_filtered[0], x_filtered[-1], 5*len(x_filtered))
new_y_real = f_real(new_x)
new_y_imag = f_imag(new_x)

# Объединяем вещественную и мнимую части обратно в комплексные числа
new_y = new_y_real + 1j*new_y_imag

# Отображаем исходные данные и интерполированные данные на графике
plt.figure()
plt.plot(x_real, x_imag, 'o', label='Исходные данные')
plt.plot(new_y_real, new_y_imag, '-', label='Интерполированные данные')
plt.xlabel('Re')
plt.ylabel('Im')
plt.legend()
plt.grid()
plt.show()

