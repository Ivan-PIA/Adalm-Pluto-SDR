import numpy as np

# Определение оригинальных символов QPSK
original_symbols = np.array([1+1j, -1+1j, -1-1j, 1-1j])

# Генерация случайных символов QPSK для 20 точек
np.random.seed(0)
received_symbols = np.random.choice(original_symbols, 20)

# Функция для расчета EVM для каждой точки QPSK
def calculate_evm(original_symbols, received_symbols):
    evm = np.mean(np.abs(original_symbols - received_symbols)**2) / np.mean(np.abs(original_symbols)**2) * 100
    
    return evm

# Вызов функции для расчета EVM
evm_value = calculate_evm(original_symbols, received_symbols)

# Вывод результата
print("Значение EVM: %.2f%%" % evm_value)