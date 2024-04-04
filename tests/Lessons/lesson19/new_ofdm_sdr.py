import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic

def activ_carriers(N_fft, GB_len, pilot_carriers, pilots = False):
    """
    ml.activ_carriers(64, 6, (-21, -7, 7, 21), True)

    GB - guard_band_len

    PC - pilot_carriers
        
    Возвращает массив поднесущих на которых имеются данные
    """
    fft_len = N_fft
    GB = GB_len // 2
    PilCar = pilot_carriers

    if pilots:
        activ = np.array([
                i
                for i in range(0, fft_len)
                if (i in range(GB, fft_len - GB + 1))
                and (i != fft_len/2)
            ])
    else:
        activ = np.array([
                i
                for i in range(0, fft_len)
                if (i in range(GB, fft_len - GB + 1))
                and (i not in PilCar)
                and (i != fft_len/2)
            ])
        
    #activ = activ + (self.N_fft / 2)
        
    return activ

def generate_pilot_carriers(N_fft, GB_len, N_pil):
    """
    Generates indices representing pilot subcarriers.

    Args:
        N_pilot (int): Number of pilot subcarriers.

        Returns:
            np.ndarray: Array of pilot subcarrier indices within the usable bandwidth.
    """
    usable_bandwidth = N_fft - GB_len

    pilot_spacing = int(usable_bandwidth / (N_pil - 1))  # Spacing between pilots

    # Можно менять значение от 0 до 1
    #                          ↓
    pilot_carriers = np.arange(0 + GB_len//2, N_fft - GB_len//2+1, pilot_spacing)

    for i in range(len(pilot_carriers)):
        if pilot_carriers[i] == 32:
            pilot_carriers[i] += 1
                
    # Handle potential rounding errors or edge cases
    if len(pilot_carriers) < N_pil:
        pilot_carriers = np.concatenate((pilot_carriers, [N_fft // 2 + 1]))  # Add center carrier if needed
    elif len(pilot_carriers) > N_pil:
        pilot_carriers = pilot_carriers[:N_pil]  # Truncate if there are too many

    return pilot_carriers

def delete_CP(rx_ofdm, num_carrier, cp): # удаление циклического префикса 

    rx_sig_de = np.zeros(0)

    for i in range(len(rx_ofdm)//(num_carrier+cp)):
        del_cp = rx_ofdm[i*(cp+num_carrier)+cp:(i+1)*(cp+num_carrier)]
        #print(len(del_cp))
        de_symbol = np.fft.fftshift(np.fft.fft(del_cp,num_carrier))
        rx_sig_de = np.concatenate([rx_sig_de,de_symbol])
    #print("alleeee",len(rx_sig_de))
    return rx_sig_de

def OFDM_MOD(N_fft, GB_len, N_pil, QAM , CP): # формирование OFDM символы
    pilot = complex(1,1) * 2**14
    len_data = N_fft-N_pil-GB_len

    pilot_carrier = generate_pilot_carriers(N_fft, GB_len, N_pil)
    data_carrier = activ_carriers(num_carrier, GB_len, pilot_carrier)

    count_ofdm_symbol = len(QAM) // len(data_carrier) + 1 
    ofdm = np.zeros((count_ofdm_symbol, N_fft),dtype=np.complex128)
    
    ofdm_ifft_cp = np.zeros(0)
    for j in range(count_ofdm_symbol):
            if len_data == len(QAM[j * len_data :(j+1)*len_data]):
                ofdm[j][pilot_carrier] = pilot
                ofdm[j][data_carrier] = QAM[j * len_data :(j+1)*len_data]
                ifft_ofdm = np.fft.ifft((np.fft.fftshift(ofdm[j])),N_fft)
                ofdm_ifft_cp = np.concatenate([ofdm_ifft_cp, ifft_ofdm[-CP:], ifft_ofdm])
            else:
                data_carrier1 = data_carrier[:len(QAM[j * len_data :(j+1)*len_data])]
                ofdm[j][pilot_carrier] = pilot
                ofdm[j][data_carrier1] = QAM[j * len_data :(j+1)*len_data]
                ifft_ofdm = np.fft.ifft((np.fft.fftshift(ofdm[j])),N_fft)
                ofdm_ifft_cp = np.concatenate([ofdm_ifft_cp, ifft_ofdm[-CP:], ifft_ofdm])

    return ofdm_ifft_cp, data_carrier1

def correlat_ofdm(rx_ofdm, cp,num_carrier): # корреляция по циклическому префиксу 
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
    print(cor)
    ic(cor_max)
    #index = index_cor[len(index_cor)]
    #plt.figure(3)
    #plt.plot(cor.real)
    #plt.plot(cor.imag)
    #print("ind",index)
    #return (index - (cp+num_carrier))
    return index

def interpolatin_pilot(rx_pilot,pilot_carrier, rx_sync,GB_len):
    print(pilot_carrier)
    count_ofdm = len(rx_sync)
    num_carrier = len(rx_sync[0])
    
    pilot = complex(1,1) 
    Hls = rx_pilot / pilot                                                    # частотная характеристика канала на пилотах

    Hls1 = Hls.flatten()

    if 1:                                                                    
        plt.figure(7)
        plt.title("Частотная характеристика канала на пилотах")
        plt.stem(abs(Hls1), "r",label='pilot - ampl')
        plt.stem(np.angle(Hls1),label='pilot - phase')
        plt.legend(loc='upper right')

    pilot_carrier = pilot_carrier-GB_len//2                                   # индексы пилотов без защитных нулей
    print("pppp",pilot_carrier)
    #print(Hls)

    all_inter = np.zeros(0)

    ### Интерполяция ###
    for i in  range(count_ofdm):                                               # цикл по количеству ofdm символов
        x_interp = np.linspace(0, num_carrier - GB_len, num_carrier - GB_len)  # цикл по количеству ofdm символов
        interpol = np.interp(x_interp, pilot_carrier-GB_len//2, Hls[i])
        all_inter = np.concatenate([all_inter, interpol])


    #print(all_inter)
    #interpol = y_interp
    #print("len inter",len(interpol))
    interpol = interpol.flatten()
    plt.figure(8)
    plt.title('Интерполяция')
    plt.stem(abs(all_inter))
    return all_inter

def get_value_pilot(rx, index_pilot):
    rx = np.asarray(rx)
    #Hls = rx[0][index_pilot]
       
    value_pilot = np.array([np.take(row, index_pilot) for row in rx])
    
    return value_pilot    

def Classen_Freq(ofdm,  Nfft, pilot, pilot_carrier):     #Частотная синхронизация 
    eps_all = []
    eps_tran = []
    off = []
    eps = 0
    #index_pilot = index_pilot[1:]
    #max_eps = np.max(eps_all)
    print("pilot ",pilot_carrier)
    for sym in range(len(ofdm)-1):
        for offset in range(-10,10):
            eps_a = 0
            eps_f1 = 0
            pilot_carrier1 = pilot_carrier + offset
            e1 = ofdm[sym][pilot_carrier1]                    # все пилоты одного символа
            e2 = np.conjugate(ofdm[sym+1][pilot_carrier1])    # все пилоты соседнего символа
            
            for pil in range(len(pilot_carrier)):
                eps_a += abs(pilot * np.conjugate(pilot) * e1[pil] * np.conjugate(e2[pil]))/ (len(ofdm[0]*2*np.pi))
                eps_f1 += np.angle(pilot * np.conjugate(pilot) * e1[pil] * np.conjugate(e2[pil])) / (len(ofdm[0]*2*np.pi*1))
            eps_all.append(eps_a)
            eps_tran.append(eps_f1)            
           


    #eps_norm = eps_all / np.max(eps_all)
    max_eps = np.max(eps_all)

    ic(eps_tran)

    ind_max = np.argmax(eps_all)


    of_drob = eps_tran[ind_max]
    ind_max-=24
    
    ofset_fin = ind_max + of_drob

    print("max off", ofset_fin)
    ic(eps_all)
    for i in range(len(ofdm)): # количество ofdm символов
  
        for n in range(0,Nfft):
            ofdm[i][n] = ofdm[i][n] * np.exp(-1j * 2 * np.pi * (0)/Nfft * n)
           
            #print(n)
  
    return ofdm      



def Freq_Correction(ofdm, Nfft, cp): # для матрицы

    for i in range(len(ofdm)//(Nfft+cp)): # 
        
        e1 = ofdm[i][:cp]
        e2 = ofdm[i+1][:cp]
        sum = abs(np.sum(np.conjugate(e1) * e2)/(np.pi*2))
        ic(sum)

    for i in range(len(ofdm)//(Nfft)): # количество ofdm символов
        for n in range(0, Nfft):
            ofdm[i][n] = ofdm[i][n] * np.exp(-1j * 2 * np.pi * (sum/Nfft) * n)   

    return ofdm.flatten()





sdr = standart_settings("ip:192.168.2.1", 1e6, 1e3)
sdr2 = standart_settings("ip:192.168.3.1", 1e6, 1e3)

num_carrier = 64

N_pilot = 10
GB_len = 28
CP = 16

mes = "lalalavavavavavfjkafbaldj123456781lalalavavavavavfjkafbaldj12erwdgns" #2 ofdm 
mes2 = "A small sfsdfsdfsf"
bit = randomDataGenerator(2400)
bit1 = text_to_bits(mes2)


qpsk1 = QPSK(bit1)
len_qpsk = len(qpsk1)
print(len_qpsk)



pilot_carrier = generate_pilot_carriers(num_carrier, GB_len, N_pilot)
data_carrier = activ_carriers(num_carrier, GB_len, pilot_carrier)
print(pilot_carrier)
print(data_carrier)

ofdm, last_ofdm_data = OFDM_MOD(num_carrier, GB_len, N_pilot, qpsk1, CP)


tx_signal(sdr,2000e6,0,ofdm)
rx_sig = rx_signal(sdr2,2000e6,20,30)

rxMax = max(rx_sig.real)
rx_sig = rx_sig / rxMax

index = correlat_ofdm(rx_sig,CP,num_carrier)
#index = correlate_frame(rx_sig, len(pss), len_pack)

rx_ofdm = rx_sig[index:]
#rx_ofdm = rx_sig[len(pss):]
rx_ofdm = rx_ofdm[:len(ofdm)]

#ofdm2 = rx_ofdm.reshape(len(rx_ofdm)//(num_carrier+CP),num_carrier+CP)

#rx_ofdm = Freq_Correction(ofdm2, num_carrier, CP)




del_cp = delete_CP(rx_ofdm, num_carrier, CP)

pilot = complex(1,1)

ofdm1 = del_cp.reshape(len(del_cp)//num_carrier,num_carrier)

#ofdm1 = Classen_Freq(ofdm1,num_carrier,pilot, pilot_carrier)

#del_cp = ofdm1.flatten()
plot_QAM(del_cp, "Befor Interpolation")



#ofdm1 = Classen_Freq(ofdm1,num_carrier,pilot, pilot_carrier)

#print(ofdm1)
value_pilot = get_value_pilot(ofdm1,pilot_carrier)
inter = interpolatin_pilot(value_pilot,pilot_carrier, ofdm1, GB_len)

#inter = interpol_pilots(rx_ofdm, num_carrier,GB_len, pilot_carrier, CP)

#plt.figure(2)
#plot_QAM(inter, "AFTER Interpolation")


#plt.figure(1)
#plt.plot(abs(np.fft.fft(ofdm)))
data_carrier1 = activ_carriers(num_carrier, GB_len, pilot_carrier, pilots = True)

print("ll",data_carrier1)
data_pilot = np.zeros(0)

for i in range(len(ofdm1)):
        #print(i)
        qpsk = ofdm1[i][data_carrier1]
        data_pilot = np.concatenate([data_pilot, qpsk])



#inter = interpol_pilots(good, num_carrier,GB_len, pilot_carrier)

data_pilot = data_pilot/ inter


#data_carrier2 = data_carrier - GB_len//2 - 1

#print(inter)
#print("equal = ", data_pilot)

plot_QAM(data_pilot, "AFTER Interpolation")


# закинуть в функцию
data_carrier1_not_pilot = activ_carriers(num_carrier, GB_len, pilot_carrier) 


for i in range(len(data_carrier1_not_pilot)):
    if data_carrier1_not_pilot[i] > num_carrier//2:
        data_carrier1_not_pilot[i] -=1

data_carrier1_not_pilot = data_carrier1_not_pilot - GB_len//2
print("not_pilot ",data_carrier1_not_pilot)  

ofdm2 = data_pilot.reshape(len(data_pilot)//(num_carrier-GB_len),num_carrier-GB_len)

print("oly_pilot: ",pilot_carrier-GB_len//2)

#print("ofdm2 = ", len(ofdm2),len(ofdm2[0]), ofdm2)

data = np.zeros(0)
for i in range(len(ofdm2)):
        #print(i)
        qpsk = ofdm2[i][data_carrier1_not_pilot]
        data = np.concatenate([data, qpsk])



data = data[abs(data) >= 0.3] # удаление нулей из последнего ofdm


plot_QAM(data, "qpsk")



deqpsk = DeQPSK(data)
text = bits_array_to_text(deqpsk)
print(text)
plt.show()
