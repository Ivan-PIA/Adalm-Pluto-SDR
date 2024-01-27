import time

import adi
import matplotlib.pyplot as plt



sdr = adi.Pluto("ip:192.168.2.1")


sdr.rx_lo = int(2000e6 + 2e6 * 4)
sdr.tx_lo = int(2000e6 + 2e6 * 4)
sdr.sample_rate = 1e6
sdr.rx_buffer_size = 10000
sdr.tx_cyclic_buffer = True



def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):                      # перевод из текста в биты
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



word = 'andrey'


bits = text_to_bits(word)+"1"
text = text_from_bits(bits)
print(bits)
print(text)
bit_num_samples = 20


# bit_1 = [2**14 + 1j * 2**14 for i in range(0,bit_num_samples)]
# bit_0 = [1 +1j * 1 for i in range(0,bit_num_samples)]
# print(bit_0)

# def AM():                    
#     data = []
   
#     for i in range(len(bits)):
        
#         if bits[i]=='0':
           
#             data+=bit_0
#         elif bits[i]=='1':
            
#             data+=bit_1
#     return data


# sample = AM()
# plt.plot(sample)
# print(sample)

# while(1):
#     print(1)
#     sdr.tx(sample)
#     time.sleep(2)
#     sdr.tx_destroy_buffer()