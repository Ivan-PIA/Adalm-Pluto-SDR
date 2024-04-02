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


def delete_CP(rx_ofdm, num_carrier, cp):

    rx_sig_de = np.zeros(0)

    for i in range(len(rx_ofdm)//(num_carrier+cp)):
        del_cp = rx_ofdm[i*(cp+num_carrier)+cp:(i+1)*(cp+num_carrier)]
        #print(len(del_cp))
        de_symbol = np.fft.fftshift(np.fft.fft(del_cp,num_carrier))
        rx_sig_de = np.concatenate([rx_sig_de,de_symbol])
    #print("alleeee",len(rx_sig_de))
    return rx_sig_de


def OFDM_MOD(N_fft, GB_len, N_pil, QAM , CP):
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

def interpolatin_pilot(rx_pilot,pilot_carrier, rx_sync,GB_len):
    print(pilot_carrier)
    count_ofdm = len(rx_sync)
    num_carrier = len(rx_sync[0])
    
    pilot = complex(1,1) 
    Hls = rx_pilot / pilot

    Hls1 = Hls.flatten()


    plt.figure(7)
    plt.title("Частотная характеристика канала на пилотах")
    plt.stem(abs(Hls1), "r",label='pilot - ampl')
    plt.stem(np.angle(Hls1),label='pilot - phase')
    plt.legend(loc='upper right')

    pilot_carrier = pilot_carrier-GB_len//2
    print("pppp",pilot_carrier)
    #print(Hls)

    all_inter = np.zeros(0)
    for i in  range(count_ofdm):
        x_interp = np.linspace(0, num_carrier- GB_len, num_carrier- GB_len)  
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

def Classen_Freq(rx_sig,  Nfft, pilot, index_pilot):
    eps_all = []
    eps = 0
    #index_pilot = index_pilot[1:]
    
    
#
    #max_eps = np.max(eps_all)
    ic(eps_all)
    for i in range(len(rx_sig)//(Nfft)):
        n_new = 0 
        for n in range(i*(Nfft),(i+1) * (Nfft)):
            rx_sig[n] = rx_sig[n] * np.exp(-1j * 2 * np.pi * 2/Nfft * n_new)
            n_new += 1 
            #print(n)
        n_new = 0 
    return rx_sig    

def Freq_Correction(rx_ofdm, Nfft, cp):

    for i in range(len(rx_ofdm)//(Nfft+cp)):
        
        e1 = rx_ofdm[(i * (Nfft + cp)) :( i * (Nfft + cp) + cp)]
        e2 = rx_ofdm[(i * (Nfft + cp) + Nfft):(i * (Nfft + cp) + (Nfft+cp))]
        sum = abs(np.sum(np.conjugate(e1) * e2)/(np.pi*2))
        ic(sum)

        n_new = 0 
        for n in range(i*(Nfft+cp) + cp,(i+1) * (Nfft+cp)):
            rx_ofdm[n] = rx_ofdm[n] * np.exp(-1j * 2 * np.pi * (0.73/Nfft) * n_new)
            n_new += 1 
            #print(n)
        n_new = 0    
    return rx_ofdm





sdr = standart_settings("ip:192.168.2.1", 1e6, 1e3)
#sdr2 = standart_settings("ip:192.168.3.1", 1e6, 1e3)


num_carrier = 64

N_pilot = 10
GB_len = 28
CP = 16

mes = "lalalavavavavavfjkafbaldj123456781lalalavavavavavfjkafbaldj12erwdgns" #2 ofdm 
mes2 = "A small text 1 2 3 4 5"
bit = randomDataGenerator(240)
bit1 = text_to_bits(mes2)


qpsk1 = QPSK(bit1)
len_qpsk = len(qpsk1)
print(len_qpsk)

qpsk = np.ones(256) * complex(0.7,0.7)

pilot_carrier = generate_pilot_carriers(num_carrier, GB_len, N_pilot)
data_carrier = activ_carriers(num_carrier, GB_len, pilot_carrier)
print(pilot_carrier)
print(data_carrier)

ofdm, last_ofdm_data = OFDM_MOD(num_carrier, GB_len, N_pilot, qpsk1, CP)


tx_signal(sdr,1900e6,0,ofdm)
rx_sig = rx_signal(sdr,1900e6,20,30)

rxMax = max(rx_sig.real)
#rx_sig = rx_sig / rxMax

index = correlat_ofdm(rx_sig,CP,num_carrier)
#index = correlate_frame(rx_sig, len(pss), len_pack)

rx_ofdm = rx_sig[index:]
#rx_ofdm = rx_sig[len(pss):]
rx_ofdm = rx_ofdm[:len(ofdm)]

#rx_ofdm = Freq_Correction(rx_ofdm,num_carrier,CP)

del_cp = delete_CP(rx_ofdm, num_carrier, CP)

pilot = complex(1,1)

#del_cp = Classen_Freq(del_cp,num_carrier,pilot, pilot_carrier)

plt.figure(1)
plot_QAM(del_cp, "Befor Interpolation")

ofdm1 = del_cp.reshape(len(del_cp)//num_carrier,num_carrier)
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
plt.figure(2)
plot_QAM(data_pilot, "AFTER Interpolation")

data_carrier1_not_pilot = activ_carriers(num_carrier, GB_len, pilot_carrier) 


for i in range(len(data_carrier1_not_pilot)):
    if data_carrier1_not_pilot[i] > num_carrier//2:
        data_carrier1_not_pilot[i] -=1

data_carrier1_not_pilot = data_carrier1_not_pilot - GB_len//2
print("not_pilot ",data_carrier1_not_pilot)  

ofdm2 = data_pilot.reshape(len(data_pilot)//(num_carrier-GB_len),num_carrier-GB_len)

print("oly_pilot: ",pilot_carrier-GB_len//2)

print("ofdm2 = ", len(ofdm2),len(ofdm2[0]), ofdm2)

data = np.zeros(0)
for i in range(len(ofdm2)):
        #print(i)
        qpsk = ofdm2[i][data_carrier1_not_pilot]
        data = np.concatenate([data, qpsk])


# print(ofdm2)

# good2 = np.zeros(0)

# for i in range(len(ofdm2)):
#         #print(i)
#         qpsk = ofdm2[i][data_carrier2]
#         good2 = np.concatenate([good2, qpsk])


data = data[abs(data) >= 0.3]

plt.figure(3)
plot_QAM(data, "qpsk")



deqpsk = DeQPSK(data)
text = bits_array_to_text(deqpsk)
print(text)
#print(len(good2))
plt.show()
