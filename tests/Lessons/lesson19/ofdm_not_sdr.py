import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic


def QPSK(bit_mass):
	ampl = 2**14
	if (len(bit_mass) % 2 != 0):
		print("QPSK:\nError, check bit_mass length", len(bit_mass))
		raise "error"
	else:
		sample = [] # массив комплексных чисел
		for i in range(0, len(bit_mass), 2):
			b2i = bit_mass[i]
			b2i1 = bit_mass[i+1]
			real = (1 - 2 * b2i) / np.sqrt(2)
			imag = (1 - 2 * b2i1) / np.sqrt(2)
			sample.append(complex(real, imag))
		sample = np.asarray(sample)
		sample = sample * ampl
		return sample

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return np.asarray(list(map(int,bits.zfill(8 * ((len(bits) + 7) // 8)))))


def delete_CP(rx_ofdm, num_carrier, cp):

    rx_sig_de = np.zeros(0)

    for i in range(len(rx_ofdm)//(num_carrier+cp)):
        del_cp = rx_ofdm[i*(cp+num_carrier)+cp:(i+1)*(cp+num_carrier)]
        print(len(del_cp))
        de_symbol = np.fft.fft(del_cp,num_carrier)
        rx_sig_de = np.concatenate([rx_sig_de,de_symbol])
    print("alleeee",len(rx_sig_de))
    return rx_sig_de

def fill_zeros(arr1, num):
    num1 = int(np.ceil(len(arr1)/num)*num)
    zeros = np.zeros(num1 - len(arr1))
    if len(arr1) < num1:
        arr1 = np.concatenate([arr1,zeros])
    else:
        print("длина должна быть больше")
    return arr1

def gen_ofdm_symbols(qpsk1,num_carrier,cp):

    ofdm_symbols = np.zeros(0)
    qpsk = fill_zeros(qpsk1,num_carrier)
    print("qpsk",len(qpsk))
    for i in range(len(qpsk)//num_carrier):
        ofdm_symbol = np.fft.ifft(qpsk[i * num_carrier : (i+1) * num_carrier], num_carrier)
        ofdm_symbols = np.concatenate([ofdm_symbols, ofdm_symbol[-cp:], ofdm_symbol])
        
    return ofdm_symbols


def norm_corr(x,y):
    #x_normalized = (cp1 - np.mean(cp1)) / np.std(cp1)
    #y_normalized = (cp2 - np.mean(cp2)) / np.std(cp2)

    c_real = np.vdot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
    c_imag = np.vdot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
    
    return c_real+1j*c_imag
    
    

def correlat_ofdm(rx_ofdm, cp,num_carrier):
    max = 0
    rx1 = rx_ofdm
    cor = []
    cor_max = []
    for j in range(len(rx1)):
        corr_sum = norm_corr(rx1[:cp],np.conjugate(rx1[num_carrier:num_carrier+cp]))
        #print(corr_sum)
        cor.append(corr_sum)
        if corr_sum > max and (corr_sum.imag > 0.9 or corr_sum.real > 0.9):
            cor_max.append(corr_sum)
            max = corr_sum
            #print(np.round(max))
            index = j
        rx1= np.roll(rx1,-1)

    cor  = np.asarray(cor)
    ic(cor_max)
    plt.figure(3)
    plt.plot(cor.real)
    plt.plot(cor.imag)
    print("ind",index)
    #return (index - (cp+num_carrier))
    return index

def add_pilot(ofdm,num_carrier,pilot):
    pass



def PLL(conv):
    mu = 1# коэфф фильтра 
    theta = 0.40 # начальная фаза
    phase_error = np.zeros(len(conv))  # фазовая ошибка
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        theta_hat = np.angle(conv[n])  # оценка фазы
        #print(theta_hat)
        phase_error[n] = theta_hat - theta  # фазовая ошибка
        output_signal[n] = conv[n] * np.exp(-1j * theta)  # выходной сигнал
        theta = theta + mu * phase_error[n]  # обновление

    return output_signal





num_carrier = 32
cp = 8
bit = text_to_bits("lalalavavavavavfjkafbaldjgvbcljbphlskjlskkck,dnkhehdvbhdfghjk")
print(len(bit))

qpsk1 = QPSK(bit)
#qpsk1 = np.repeat(qpsk1,num_carrier)
print("len qpsk = ",len(qpsk1))


ofdm_symbols = gen_ofdm_symbols(qpsk1, num_carrier,cp)

plt.figure(1)
plt.plot(np.fft.fftshift(abs(np.fft.fft(np.ravel(ofdm_symbols), int(1e6)))))

print("len ofdm_simbols = ",len(ofdm_symbols))

len_pack = len(ofdm_symbols)

noise = np.random.normal(0,10,len(ofdm_symbols))

rx_ofdm = ofdm_symbols + noise + 1j * noise



##############
noise = np.random.normal(0,100,len(ofdm_symbols)) 
noise = noise + noise * 1j

rx_ofdm = np.concatenate([noise,rx_ofdm,rx_ofdm,noise])
h = np.ones(5)
rx_ofdm = np.convolve(rx_ofdm,h)
#print(rx_ofdm)
rx_ofdm = np.roll(rx_ofdm,0)
index = 0
index = correlat_ofdm(rx_ofdm, cp, num_carrier)
print("index corr = ",index)

rx_ofdm = rx_ofdm[index:]
rx_ofdm = rx_ofdm[:len_pack]

print("rx_ofdm = ", len(rx_ofdm))


rx_sig_de = delete_CP(rx_ofdm, num_carrier, cp)

print("rx_sig_de = ", len(rx_sig_de))

rx_sig_de = np.round(rx_sig_de)

rx_sig_de = rx_sig_de[abs(rx_sig_de) >= 500]

print("len demodel = ", len(rx_sig_de))

#rx_sig_frec = PLL(nonzero_elements)


#rx_sig_frec = PLL2(rx_sig_frec)
#print("len demodel = ", len(rx_sig_frec))


#plt.figure(1)

#plt.scatter(rx_sig_frec.real, rx_sig_frec.imag)
plt.figure(2)

plt.scatter(rx_sig_de.real, rx_sig_de.imag)
#plt.plot(rx_sig_de)


deqpsk = DeQPSK(rx_sig_de)






print(len(deqpsk))

print(bit)
text = text_from_bits(bit)

print(text)
#plt.figure(1)
#plt.plot(rx)

#dedata = np.fft.fft(rx,num_carrier)

#plt.figure(2)
#plt.scatter(dedata.real,dedata.imag)

plt.show()



