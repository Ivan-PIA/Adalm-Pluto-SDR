import numpy as np

def crc16_bit(data):
    crc = 0xFFFF
    for bit in data:
        crc = crc ^ (int(bit) << 8)
        for _ in range(0, 8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    crc = crc & 0xFFFF

    crc_rep = bin(crc)[2:]
    crc_array = [int(bit) for bit in crc_rep]
    return np.asarray(crc_array)

# Пример использования
data_bits = [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1,1,1,0,1,0,0,0,0,1]
result = crc16_bit(data_bits)
print(len(result))