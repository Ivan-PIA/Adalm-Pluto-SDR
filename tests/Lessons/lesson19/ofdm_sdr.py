import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic


import sys

def fft(ofdm_symbols):
    fft = []
    len_c = np.shape(ofdm_symbols)[0]
    for i in range(len_c):
        if len_c == 1:
            zn = np.fft.fftshift(np.fft.fft(ofdm_symbols))
        else:
            zn = np.fft.fftshift(np.fft.fft(ofdm_symbols[i]))
                

                
        fft.append(zn)
                

        return fft

def delete_CP(rx_ofdm, num_carrier, cp):

    rx_sig_de = np.zeros(0)

    for i in range(len(rx_ofdm)//(num_carrier+cp)):
        del_cp = rx_ofdm[i*(cp+num_carrier)+cp:(i+1)*(cp+num_carrier)]
        #print(len(del_cp))
        de_symbol = np.fft.fft(del_cp,num_carrier)
        rx_sig_de = np.concatenate([rx_sig_de,de_symbol])
    #print("alleeee",len(rx_sig_de))
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
    

def indexs_of_CP(rx, fft_len, cp):
    """
    Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
    """

        
    corr = [] # Массив корреляции 
    for i in range(len(rx)):
        o = norm_corr(rx[:cp], rx[fft_len:fft_len+cp])
        corr.append(abs(o))
        rx = np.roll(rx, 1)
            
    corr = np.array(corr) / np.max(corr) # Нормирование

    if corr[0] > 0.98:
        max_len_cycle = len(corr)
    else:
        max_len_cycle = len(corr)-(fft_len+cp)

    arr_index = [] # Массив индексов максимальных значений corr
    for i in range(0, max_len_cycle, (fft_len+cp)):
        max = np.max(corr[i : i+(fft_len+cp)])
        if max > 0.9: 
            ind = i + np.argmax(corr[i : i+(fft_len+cp)])
            if ind < (len(corr)-(fft_len+cp)):
                arr_index.append(ind)
        
    ### DEBUG
    # print(arr_index)
    # print(corr)
    # from mylib import cool_plot
    # cool_plot(corr, title='corr', show_plot=False)
        
    return arr_index

def indiv_symbols(ofdm, cp, N_fft):
    
    all_sym = N_fft + cp
        
    index = indexs_of_CP(ofdm, N_fft, cp)
    symbols = []
    for ind in index:
        symbols.append(ofdm[ind+cp : ind+all_sym])
    
    return symbols



def correlat_ofdm(rx_ofdm, cp,num_carrier):
    max = 0
    rx1 = rx_ofdm
    cor = []
    cor_max = []
    for j in range(len(rx1)):
        corr_sum =abs(norm_corr(rx1[:cp],np.conjugate(rx1[num_carrier:num_carrier+cp])))
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

def add_pilot(qpsk,pilot,step_pilot): # добавление pilot с заданым шагом (pilot - переменная, одно значение пилота)

    step_pilot -= 1
    newarr = []
    newarr.append(pilot)

    for i in range( len(qpsk) ):
        newarr.append( qpsk[i] )
        
        if (i + 1) % step_pilot == 0:
            newarr.append(pilot)
    
    return np.asarray(newarr)

def del_pilot(ofdm,pilot_carrier):

    ofdm = np.delete(ofdm,pilot_carrier)

    return ofdm

def Freq_Correction(rx_ofdm, Nfft, cp):

    for i in range(len(rx_ofdm)//(Nfft+cp)):
        
        e1 = rx_ofdm[(i * (Nfft + cp)) :( i * (Nfft + cp) + cp)]
        e2 = rx_ofdm[(i * (Nfft + cp) + Nfft):(i * (Nfft + cp) + (Nfft+cp))]
        sum = np.sum(np.conjugate(e1) * e2)/(np.pi*2)


        n_new = 0 
        for n in range(i*(Nfft+cp) + cp,(i+1) * (Nfft+cp)):
            rx_ofdm[n] = rx_ofdm[n] * np.exp(-1j * 2 * np.pi * (sum/Nfft) * n_new)
            n_new += 1 
            print(n)
        n_new = 0    
    return rx_ofdm

def PLL(conv):
    mu = 1# коэфф фильтра 
    theta = 0 # начальная фаза
    phase_error = np.zeros(len(conv))  # фазовая ошибка
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        theta_hat = np.angle(conv[n])  # оценка фазы
        #print(theta_hat)
        phase_error[n] = theta_hat - theta  # фазовая ошибка
        output_signal[n] = conv[n] * np.exp(-1j * theta)  # выходной сигнал
        theta = theta + mu * phase_error[n]  # обновление

    return output_signal

def FLL(conv):
    mu = 0.01
    omega = 0.8 # TODO: нужно протестировать для разных сигналов, пока непонятно, работает ли этот коэффициент для всех QPSK-сигналов
    freq_error = np.zeros(len(conv))
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        angle_diff = np.angle(conv[n]) - np.angle(output_signal[n-1]) if n > 0 else 0
        freq_error[n] = angle_diff / (2 * np.pi)
        omega = omega + mu * freq_error[n]
        output_signal[n] = conv[n] * np.exp(-1j * omega)
    return output_signal

def correlate_frame(signal, pss):
    max = 0
    for j in range(len(signal)-len(pss)):
        corr_sum = np.correlate(pss, signal[:(len(pss))])
        if corr_sum > max:
            max = corr_sum
            index = j
        signal = np.roll(signal,-1)
    return index


def get_index_pilot(rx_ofdm):
    index_pilot = []
    for i in range(len(rx_ofdm)):
        if abs(rx_ofdm[i].imag) > 4 or abs(rx_ofdm[i].real) > 4:
            index_pilot.append(i) 
    return np.asarray(index_pilot)

def OFDM_MODULATOR(qpsk1, num_carrier, cp, step_pilot, pss ):
    pilot = complex(5,5)

    #pilot_carrier = np.arange(0,len(qpsk1),step_pilot)# for del pilot

    print("len qpsk = ",len(qpsk1))


    added_pilot = add_pilot(qpsk1,pilot,step_pilot) * 2**14
    
    ic(added_pilot)

    pilot_carrier = np.arange(0,len(added_pilot),step_pilot)# for del pilot
    del_p = del_pilot(added_pilot, pilot_carrier)
    ic(del_p)
    plt.figure(2)
    plt.title("On TX")
    plt.scatter(added_pilot.real, added_pilot.imag)
    plt.figure(5)
    plt.title("On TX2")
    plt.scatter(del_p.real, del_p.imag)

    ofdm_symbols = gen_ofdm_symbols(added_pilot, num_carrier,cp)
    #print(np.ravel(ofdm_symbols))

    print("len ofdm_simbols = ",len(ofdm_symbols))
    pss = pss * 2**14
    #ofdm_symbols = np.concatenate([pss, ofdm_symbols])
    return ofdm_symbols, added_pilot


def OFDM_DEMODULATOR(rx_sig, num_carrier, cp, len_pack, len_add_pilot, pss ):
    pilot = complex(4,4)
    
    rx_ofdm = indiv_symbols(rx_sig, cp, num_carrier)


    #rx_ofdm = rx_sig[index:]
    #rx_ofdm = rx_ofdm[:len_pack]

    #rx_ofdm = Freq_Correction(rx_ofdm,num_carrier, cp)

    pilot_carrier = np.arange(0,len_add_pilot,step_pilot) # for del pilot

    rx_sig_de = fft(rx_ofdm)
    print(rx_sig_de)
    #pilot_index = get_index_pilot(rx_sig_de)
    #rx_sig_de = PLL(rx_sig_de)
    #rx_sig_de = FLL(rx_sig_de)
    
    #print("pilot index =  ",pilot_index)
    #print("count pilot = ", len(pilot_index))
    #rx_sig_de = del_pilot(rx_sig_de, pilot_carrier)
    ic(rx_sig_de)
    
    #rx_sig_de = PLL(rx_sig_de)
    #rx_sig_de = FLL(rx_sig_de)
    print("rx_ofdm = ",len(rx_sig_de))


    #rx_sig_de = rx_sig_de[abs(rx_sig_de) >= 0.50]
    print("qpsk = ",len(rx_sig_de))

    plt.figure(1)
   
    plt.scatter(rx_sig_de.real, rx_sig_de.imag, s = 5)  

    return rx_sig_de  


sdr = standart_settings("ip:192.168.2.1", 1e6, 1e3)

#sdr2 = standart_settings("ip:192.168.3.1", 1e6, 1e3)

num_carrier = 64
cp = 16
step_pilot = 10


#qpsk1 = np.repeat(qpsk1,num_carrier)

pss = np.array([1, -1, -1,  1, -1, -1, -1, -1,  1,  1, -1, -1, -1,  1,  1, -1,
                    1, -1,  1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  1, -1, -1,
                    1, -1, -1,  1, -1,  1, -1, -1, -1,  1, -1,  1,  1,  1, -1, -1,
                    1,  1, -1,  1,  1,  1, -1,  1,  1,  1,  1,  1,  1, -1,  1,  1,
                   -1,  1,  1, -1, -1,  1, -1,  1,  1, -1, -1, -1, -1,  1, -1, -1,
                   -1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1,  1,  1,  1, -1,
                   -1, -1,  1, -1, -1,  1,  1,  1, -1,  1, -1,  1,  1, -1,  1, -1,
                   -1, -1, -1, -1,  1, -1,  1, -1,  1, -1,  1,  1,  1,  1, -1])

mes = "lalalavavavavavfjkafbaldjgvbcljbphlskjlskkck,dnkhehdvbh"

bit = text_to_bits("lalalavavavavavfjkafbaldjgvbcljbphlskjlskkck,dnkhehdvbh")

qpsk1 = QPSK(bit)
len_qpsk = len(qpsk1)
ofdm_symbols, added_pilot  = OFDM_MODULATOR(qpsk1, num_carrier,cp,step_pilot, pss)
len_added_pilot = len(added_pilot)


plt.figure(4)
plt.plot(np.fft.fftshift(abs(np.fft.fft(np.ravel(ofdm_symbols), int(1e6)))))
len_pack = len(ofdm_symbols)

#ofdm_symbols = ofdm_symbols * 2**10


tx_signal(sdr,2e9,0,ofdm_symbols)
rx_sig = rx_signal(sdr,2e9,20,30)

rxMax = max(rx_sig.real)
rx_sig = rx_sig / rxMax

#print("sigg",sys.getsizeof(rx_sig[10]))


##########
#DEMODULATOR#
##########

rx_sig_de = OFDM_DEMODULATOR(rx_sig, num_carrier, cp, len_pack , len_added_pilot, pss)



#deqpsk = DeQPSK(rx_sig_de)



#print("j,fklf = ",len(deqpsk))
#ic(deqpsk)
#deqpsk = list(deqpsk)
#print(deqpsk)
#print(bit)
#text = text_from_bits(deqpsk)

#print(text)
#if mes == text:
    #print("Worker coooooollll")
plt.show()




