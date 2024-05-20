import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic
from viterbi import Viterbi

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

def gen_ofdm_symbols(qpsk1,num_carrier,cp, pss):
    count_ofdm = 0
    ofdm_symbols = np.zeros(0)
    qpsk = fill_zeros(qpsk1,num_carrier)
    print("qpsk",len(qpsk))
    for i in range(len(qpsk)//num_carrier):
        count_ofdm +=1
        ofdm_symbol = np.fft.ifft((qpsk[i * num_carrier : (i+1) * num_carrier]), num_carrier) 
        ofdm_symbols = np.concatenate([ofdm_symbols, ofdm_symbol[-cp:], ofdm_symbol])
    #ofdm_symbols = np.concatenate([pss, ofdm_symbols])
    print("колличество офдм символов", count_ofdm)
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
    index_cor = []
    for j in range(len(rx1)):
        corr_sum =abs(norm_corr(rx1[:cp],np.conjugate(rx1[num_carrier:num_carrier+cp])))
        #print(corr_sum)
        cor.append(corr_sum)
        if corr_sum > max and (corr_sum.imag > 0.98 or corr_sum.real > 0.98):
            cor_max.append(corr_sum)
            max = corr_sum
            #print(np.round(max))
            index = j
            index_cor.append(index)
        rx1= np.roll(rx1,-1)

    cor  = np.asarray(cor)
    ic(cor_max)
    #index = index_cor[len(index_cor)]
    #plt.figure(3)
    #plt.plot(cor.real)
    #plt.plot(cor.imag)
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
            #if i%2 == 0:
                #newarr.append(pilot)
            #else:
                #newarr.append(-pilot)
        
        
    return np.asarray(newarr)

def del_pilot(ofdm,pilot_carrier):

    ofdm = np.delete(ofdm,pilot_carrier)

    return ofdm

def Freq_Correction(rx_ofdm, Nfft, cp):

    for i in range(len(rx_ofdm)//(Nfft+cp)):
        
        e1 = rx_ofdm[(i * (Nfft + cp)) :( i * (Nfft + cp) + cp)]
        e2 = rx_ofdm[(i * (Nfft + cp) + Nfft):(i * (Nfft + cp) + (Nfft+cp))]
        sum = abs(np.sum(np.conjugate(e1) * e2)/(np.pi*2))
        ic(sum)

        n_new = 0 
        for n in range(i*(Nfft+cp) + cp,(i+1) * (Nfft+cp)):
            rx_ofdm[n] = rx_ofdm[n] * np.exp(-1j * 2 * np.pi * (sum/Nfft) * n_new)
            n_new += 1 
            #print(n)
        n_new = 0    
    return rx_ofdm


def Classen_Freq(rx_sig,  Nfft, pilot, index_pilot):
    eps_all = []
    eps = 0
    index_pilot = index_pilot[1:]
    
    
    for i in range(-20,20):

        y_e = rx_sig[index_pilot]
        for j in range(len(y_e)//2):
            eps += (pilot * np.conjugate(pilot) * y_e[j] * np.conjugate(y_e[j+6]))/ (np.pi * Nfft)
            #print(j)
        
        eps_all.append(abs(eps))
        ic(index_pilot + i)
        y_e = rx_sig[index_pilot]
        eps = 0

    max_eps = np.max(eps_all)
    ic(eps_all)
    for i in range(len(rx_sig)//(Nfft)):
        n_new = 0 
        for n in range(i*(Nfft),(i+1) * (Nfft)):
            rx_sig[n] = rx_sig[n] * np.exp(-1j * 2 * np.pi * max_eps/Nfft * n_new)
            n_new += 1 
            #print(n)
        n_new = 0 
    return rx_sig    
   ## for i in range(len(rx_ofdm)//(Nfft+cp)):


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
    omega = -0.2# TODO: нужно протестировать для разных сигналов, пока непонятно, работает ли этот коэффициент для всех QPSK-сигналов
    freq_error = np.zeros(len(conv))
    output_signal = np.zeros(len(conv), dtype=np.complex128)

    for n in range(len(conv)):
        angle_diff = np.angle(conv[n]) - np.angle(output_signal[n-1]) if n > 0 else 0
        freq_error[n] = angle_diff / (2 * np.pi)
        omega = omega + mu * freq_error[n]
        output_signal[n] = conv[n] * np.exp(-1j * omega)
    return output_signal

def correlate_frame(signal, len_pss, len_frame):
    max = 0
    rx1 = signal
    cor = []
    cor_max = []
    for j in range(len(rx1)):
        corr_sum = abs(norm_corr(rx1[:len_pss],np.conjugate(rx1[len_frame:(len_frame + len_pss)])))
        #print(corr_sum)
        cor.append(corr_sum)
        if corr_sum > max and (corr_sum.imag > 0.98 or corr_sum.real > 0.98):
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
    #print("ind",index)
    #return (index - (cp+num_carrier))
    return index


def get_index_pilot(rx_ofdm):
    index_pilot = []
    for i in range(len(rx_ofdm)):
        if abs(rx_ofdm[i].imag) > 4 or abs(rx_ofdm[i].real) > 4:
            index_pilot.append(i) 
    return np.asarray(index_pilot)

#def pilot_carrier():

import cmath

def helper_ofdm_frequency_offset(rx_waveform):
    n_fft = 64
    cp_length = 16
    symb_len = n_fft + cp_length
    buff_len = len(rx_waveform)

    num_sym_per_frame = 4
    num_samp_per_frame = num_sym_per_frame * symb_len

    sample_avg_buffer = []
    if not sample_avg_buffer:
        num_frames = buff_len // num_samp_per_frame
        num_avg_cols = ((150 + num_frames) // 6) + 1  # (24+1)*6 symbol minimum for averaging
        sample_avg_buffer = [0] * (6 * num_avg_cols * symb_len)

    #corr_in = sample_avg_buffer[num_samp_per_frame:] + rx_waveform
    sample_avg_buffer = rx_waveform
    corr_in = rx_waveform
    arm1 = corr_in
    arm2 = [0] * n_fft + corr_in[-n_fft:]

    cpcorrunfilt = [a * np.conjugate(b) for a, b in zip(arm1, arm2)]
    cpcorrunfilt1 = cpcorrunfilt
    cpcorrunfilt2 = [0] * cp_length + cpcorrunfilt[:-cp_length]

    cp_corr = [a - b for a, b in zip(cpcorrunfilt1, cpcorrunfilt2)]
    cp_corr_final = [sum(cp_corr[:i + 1]) / cp_length for i in range(len(cp_corr))]

    data = [[0] * len(cp_corr_final) for _ in range(6)]
    for ii in range(6):
        data[ii] = [0] * ((ii - 1) * symb_len) + cp_corr_final[:-((ii - 1) * symb_len)]

    avg_corr = [sum(row) / 6 for row in zip(*data)]

    obj_mag_op = [abs(val) for val in avg_corr]
    obj_angle_op = [cmath.phase(val) for val in avg_corr]
    mag_output = obj_mag_op

    angle_output = [angle / (2 * cmath.pi) for angle in obj_angle_op]

    samples_for_6_symbols = 6 * symb_len
    max_op_num = len(mag_output) // samples_for_6_symbols

    mag_op_reshape = [mag_output[i:i + samples_for_6_symbols] for i in range(0, max_op_num * samples_for_6_symbols, samples_for_6_symbols)]
    angle_op_reshape = [angle_output[i:i + samples_for_6_symbols] for i in range(0, max_op_num * samples_for_6_symbols, samples_for_6_symbols)]

    max_mag_op = []
    max_ang_op = []
    for i in range(max_op_num):
        max_mag_op.append(max(mag_op_reshape[i]))
        loc = mag_op_reshape[i].index(max(mag_op_reshape[i]))
        max_ang_op.append(angle_op_reshape[i][loc])

    max_ang_op_final = [max_ang_op[i] - max_ang_op[i - 24] for i in range(24, len(max_ang_op))]
    f_off = [sum(max_ang_op_final[:i + 1]) / 24 for i in range(len(max_ang_op_final))]

    cfo_val = [[0] + f_off] * samples_for_6_symbols
    cfo_val_flat = [val for sublist in cfo_val for val in sublist]

    f_offset = cfo_val_flat[-buff_len:]
    ic(f_offset)
    return f_offset



def OFDM_MODULATOR(qpsk1, num_carrier, cp, step_pilot, pss ):
    pilot = complex(2,2)* 2**14

    #pilot_carrier = np.arange(0,len(qpsk1),step_pilot)# for del pilot

    print("len qpsk = ",len(qpsk1))


    added_pilot = add_pilot(qpsk1,pilot,step_pilot) 
    
    #ic(added_pilot)

    pilot_carrier = np.arange(0,len(added_pilot),step_pilot)# for del pilot
    del_p = del_pilot(added_pilot, pilot_carrier)
    #ic(del_p)
    #plt.figure(2)
    #plt.title("On TX")
    #plt.scatter(added_pilot.real, added_pilot.imag)
    #plt.figure(5)
    #plt.title("On TX2")
    #plt.scatter(del_p.real, del_p.imag)
    pss = pss * 2**14
    ofdm_symbols = gen_ofdm_symbols(added_pilot, num_carrier,cp, pss)
    #print(np.ravel(ofdm_symbols))

    print("len ofdm_simbols = ",len(ofdm_symbols))
    
    #ofdm_symbols = np.concatenate([pss, ofdm_symbols])
    return ofdm_symbols, added_pilot

def multiply_every_second_element(arr, num):
    result = []
    for i in range(len(arr)):
        if i % 4 == 0:
            result.append(arr[i] * num)
        else:
            result.append(arr[i])
    return np.asarray(result)

def Channel_Rating(signal, index_pilot, step, pilot):
    
    Hls = signal[index_pilot] / pilot
    #Hls = multiply_every_second_element(Hls, 2)
    if 1:  
        for i in range(len(Hls)):
            if abs(Hls[i]) < 2.5:
                Hls[i] = np.mean(Hls)
    #Hls = np.ones(len(Hls))*2
    ic(Hls)
    if 1:
        plt.figure(7)
        plt.stem(abs(Hls), "r",label='pilot - ampl')
        plt.stem(np.angle(Hls),label='pilot - phase')
        plt.legend(loc='upper right')
        print(index_pilot)
    interpol = np.zeros(0)

    #for i in range(len(Hls)-1):
        #x_interp = np.linspace(index_pilot[i], index_pilot[i+1], step)  # 100 точек между 0 и 1
        
        #print("lin", x_interp)
        # Линейная интерполяция
        #y_interp = np.interp(x_interp, index_pilot, Hls)
        #print("len yinter",len(y_interp))
        #interpol = np.concatenate([interpol, y_interp])

    x_interp = np.linspace(0, len(signal), len(signal))  # 100 точек между 0 и 1
  
    y_interp = np.interp(x_interp, index_pilot, Hls)

    interpol = y_interp
    #print("len inter",len(interpol))
    if 1:
        plt.figure(8)
        plt.title('Интерполяция')
        plt.stem(abs(interpol))
        plt.xlabel("")
        plt.ylabel("ampl")
    return interpol

def freq_correction(signal):
    n = len(signal)
    corr = np.conj(signal[:-1]) * signal[1:]  # Корреляция между соседними символами
    phase_error = np.angle(np.mean(corr))   # Оценка фазовой ошибки
    freq_error = phase_error / (2 * np.pi)  # Оценка частотной ошибки
    freq_correction_factor = np.exp(-1j * 2 * np.pi * freq_error * np.arange(n) / 64)
    signal_corrected = signal * freq_correction_factor
    return signal_corrected

def OFDM_DEMODULATOR(rx_sig, num_carrier, cp, len_pack, add_pilot, pss, step_pilot ):
    pilot = complex(2,2)
    print("----------",sys.getsizeof(rx_sig[0]))
    
    #rx_ofdm = indiv_symbols(rx_sig, cp, num_carrier)
    index = correlat_ofdm(rx_sig,cp,num_carrier)
    #index = correlate_frame(rx_sig, len(pss), len_pack)

    rx_ofdm = rx_sig[index:]
    #rx_ofdm = rx_sig[len(pss):]
    rx_ofdm = rx_ofdm[:len_pack]
    
    #rx_ofdm = Freq_Correction(rx_ofdm,num_carrier, cp)
    #rx_ofdm = helper_ofdm_frequency_offset(rx_ofdm)
    
    pilot_carrier = np.arange(0,len(add_pilot),step_pilot) # for del pilot
    
    rx_sig_de = delete_CP(rx_ofdm,num_carrier,cp)
    rx_sig_de = Classen_Freq(rx_sig_de, num_carrier,pilot, pilot_carrier)

    #rx_sig_de = PLL(rx_sig_de)
    #rx_sig_de = FLL(rx_sig_de)

    rx_sig_de_pilot = del_pilot(rx_sig_de, pilot_carrier)
    
    rx_sig_de_pilot = rx_sig_de_pilot[abs(rx_sig_de_pilot) >= 1.00]
    
    
    plot_QAM(rx_sig_de_pilot, "Befor Interpolation")

    #only_pilot = rx_sig_de[pilot_carrier]

    #print(rx_sig_de)
    #pilot_index = get_index_pilot(rx_sig_de)
    
    #rx_sig_de = FLL(rx_sig_de)
    
    #print("pilot index =  ",pilot_index)
    #print("count pilot = ", len(pilot_index))


    interpolar = Channel_Rating(rx_sig_de, pilot_carrier, step_pilot, pilot)
    rx_sig_de = rx_sig_de / interpolar
    
    rx_sig_de = del_pilot(rx_sig_de, pilot_carrier)
    rx_sig_de = rx_sig_de[abs(rx_sig_de) >= 0.4]

    #ic(rx_sig_de)
    #rx_sig_de = PLL(rx_sig_de)
    
    

    plot_QAM(rx_sig_de, "After Interpolation")


    #print("rx_ofdm = ",len(rx_sig_de))



    #rx_sig_de = rx_sig_de[abs(rx_sig_de) >= 1.00]
    print("qpsk = ",len(rx_sig_de))


    #plt.figure(1)
    #colors = range(len(rx_sig_de))
    #plt.scatter(rx_sig_de.real, rx_sig_de.imag, s=5, c=colors, cmap="prism", alpha=1)

    return rx_sig_de, rx_sig_de_pilot


sdr = standart_settings("ip:192.168.2.1", 1e6, 1e3)
sdr2 = standart_settings("ip:192.168.3.1", 1e6, 1e3)


num_carrier = 64
cp = 16
step_pilot = 8

#qpsk1 = np.repeat(qpsk1,num_carrier)

pss = np.array([1, -1, -1,  1, -1, -1, -1, -1,  1,  1, -1, -1, -1,  1,  1, -1,
                    1, -1,  1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  1, -1, -1,
                    1, -1, -1,  1, -1,  1, -1, -1, -1,  1, -1,  1,  1,  1, -1, -1,
                    1,  1, -1,  1,  1,  1, -1,  1,  1,  1,  1,  1,  1, -1,  1,  1,
                   -1,  1,  1, -1, -1,  1, -1,  1,  1, -1, -1, -1, -1,  1, -1, -1,
                   -1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1,  1,  1,  1, -1,
                   -1, -1,  1, -1, -1,  1,  1,  1, -1,  1, -1,  1,  1, -1,  1, -1,
                   -1, -1, -1, -1,  1, -1,  1, -1,  1, -1,  1,  1,  1,  1, -1])

mes = "lalalavavavavavfjkafbaldj123456781" #2 ofdm 
mes2 = "lalalavavavavavfjkafbaldj12erwdgnsh"#3 ofdm 

#dot11a_codec = Viterbi(7, [91, 121])
bit = text_to_bits(mes)

#bit = dot11a_codec.encode(bit)
#print(list(bit))
qpsk1 = QPSK(bit)
len_qpsk = len(qpsk1)
ofdm_symbols, added_pilot  = OFDM_MODULATOR(qpsk1, num_carrier,cp,step_pilot, pss)



#plt.figure(4)
#plt.plot(np.fft.fftshift(abs(np.fft.fft(np.ravel(ofdm_symbols), int(1e6)))))
len_pack = len(ofdm_symbols)

#ofdm_symbols = ofdm_symbols * 2**10


tx_signal(sdr,1900e6,0,ofdm_symbols)
rx_sig = rx_signal(sdr2,1900e6,20,3)

rxMax = max(rx_sig.real)
rx_sig = rx_sig / rxMax

#print("sigg",sys.getsizeof(rx_sig[10]))


##########
#DEMODULATOR#
##########

rx_chanel,rx_sig_de  = OFDM_DEMODULATOR(rx_sig, num_carrier, cp, len_pack , added_pilot, pss, step_pilot)



deqpsk = DeQPSK(rx_sig_de)
deqpsk2 = DeQPSK(rx_chanel)
#deqpsk = dot11a_codec.decode(deqpsk)
#deqpsk2 = dot11a_codec.decode(deqpsk2)

#print("j,fklf = ",len(deqpsk))
print(len(deqpsk))
print(deqpsk)
#deqpsk = list(deqpsk)
#print(deqpsk)
#print(bit)
text = bits_array_to_text(deqpsk)
text2 = bits_array_to_text(deqpsk2)
print("------",text,"------\n\n")
print("-",text2,"-")
#print(text)
if mes == text2:
    print("Worker coooooollll")
else:
    print("bad boy")
plt.show()




