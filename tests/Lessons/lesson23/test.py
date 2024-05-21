import numpy as np
import matplotlib.pyplot as plt

# Исходный массив данных
x = np.array([0, 14,28, 42, 56, 69])
y = np.array([269.06348649 +65.65707894j,  353.93533205 -90.46512287j, 309.54880461-154.93229348j, -149.25157174-194.20176522j ,228.93863684+133.49396981j,   79.39697279-299.96088459j])
#y = np.array([1+2j, 3+4j, 5+6j, 7+8j, -9+10j, 11+12j])
# Увеличиваем количество точек в 5 раз
new_x = np.linspace(x[0], x[-1], 74)
new_y = np.interp(new_x, x, abs(y))

# Отображаем исходные данные и интерполированные данные на графике
plt.figure()
plt.stem(abs(y), 'o', label='Исходные данные')
plt.figure()
plt.stem(abs(new_y), '-', label='Интерполированные данные')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

o = 55//2

print(o)