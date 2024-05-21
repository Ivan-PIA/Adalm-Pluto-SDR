# Чтение файла в двоичном виде и запись результатов в массив

import time
import numpy as np
def converted_file_to_bits(path_file):
    binary_data_array = []
    with open(path_file, "rb") as file:
        byte = file.read(1)
        while byte:
            binary_data_array.append(int.from_bytes(byte, byteorder="big"))
            byte = file.read(1)

    binary_list = [bin(num)[2:].zfill(8) for num in binary_data_array]  
    binary_string = ' '.join(binary_list)  
    binary_numbers = binary_string.split(' ')
    binary_array = [int(bit) for binary_number in binary_numbers for bit in binary_number]
    
    return np.asarray(binary_array)


def converted_bits_to_file(rx_bit,path_final_file):
    rx_bit = list(rx_bit)
    binary_string = ''.join(map(str, rx_bit))
    converted_array = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]

    #print(converted_array)

    with open(path_final_file, "wb") as file:
        for binary_data in converted_array:
            file.write(bytes([binary_data]))

#print(binary_data_array)

path = "C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\resurce_file\\last_love.mp3"
path_final_file = "C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\resurce_file\\1.mp3"

start = time.time()
rx_bit = converted_file_to_bits(path)
end = time.time() - start
print(end)

start = time.time()
converted_bits_to_file(rx_bit,path_final_file)
end = time.time() - start
print(end)

print(len(rx_bit))

