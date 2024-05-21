import numpy as np

# Создаем пример матрицы 3x3
matrix = np.array([[1, 2, 3,4],
        [4, 5, 6,71],
        [7, 8, 9,11],
        [74, 13, 33,22]])

# Поменять местами столбцы 0 и 2
temp = np.copy(matrix[0:2, :])

matrix[0:2, :] = matrix[2:4, :]
matrix[2:4, :] = temp


print("Матрица после перемещения столбцов:")
print(matrix)