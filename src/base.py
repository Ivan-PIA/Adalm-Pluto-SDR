import random
import numpy as np

def randomDataGenerator(size):
	data = [random.randint(0, 1) for i in range(size)]
	return data

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return np.asarray(list(map(int,bits.zfill(8 * ((len(bits) + 7) // 8)))))


def bits_array_to_text(bits_array):
    bits_string = ''.join([str(bit) for bit in bits_array])
    bits_string = bits_string.replace(" ", "")
    n = int(bits_string, 2)
    text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('latin1')
    return text

def norm_corr(x,y):
    #x_normalized = (cp1 - np.mean(cp1)) / np.std(cp1)
    #y_normalized = (cp2 - np.mean(cp2)) / np.std(cp2)

    c_real = np.vdot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
    c_imag = np.vdot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
    
    return c_real+1j*c_imag


def zadoff_chu(N=1, u=25, PSS=False):
    """
    Zadoff-Chu sequence
        N - length
        
        u - root index 25 29 34
        
        PSS [optional] - Primary synchronization signal
            N - 63 
            Len - 62
    """
    if PSS:
        N = 63
        n = np.arange(0, 31)
        ex1 = np.exp(-1j * np.pi * u * n * (n + 1) / N)
        n = np.arange(31, 62)
        ex2 = np.exp(-1j * np.pi * u * (n + 1) * (n + 2) / N)
        return np.concatenate([ex1, ex2])
    else:  
        n = np.arange(0, N)
        return np.exp(-1j * np.pi * u * n * (n + 1) / N)