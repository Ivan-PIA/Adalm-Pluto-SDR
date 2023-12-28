import numpy as np
import matplotlib.pyplot as plt



def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):                      # перевод из текста в биты
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):                    # перевод из битов в текст
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

high_ampl = 2**14
len_sample = 20
ampl_1 = [high_ampl+1j*high_ampl] * len_sample
ampl_0 = [1 + 1j] * len_sample

string = 'verstended'
bit = text_to_bits(string)
print(bit)
#bit = (10*'1')+bit+(10*'1')
str2 = '01110110011001010111001001110011011101000110010101101110011001000110010101110100'
shfr = text_from_bits(str2) 
print(shfr)
def gen_sig():
    data = []
    for i in range(len(bit)):
        
        if bit[i]=='0':
            data+=ampl_0

        if bit[i]=='1':
            data+=ampl_1

    return data

data = gen_sig()
plt.plot(gen_sig())    
#plt.show()


def decode_sig(data):
    bit1 = ''
    for i in range(len(bit)):
        if data[i] == (high_ampl+1j*high_ampl) :
            bit1+='1'
            
        if data[i] == (1+1j*1) :
            bit1+='0'
       
            
    return bit1   

#bit1 = decode_sig(data)
#print(bit1)    