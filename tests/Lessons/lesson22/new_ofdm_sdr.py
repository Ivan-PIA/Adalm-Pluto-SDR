import matplotlib.pyplot as plt
import numpy as np
from context import *
from icecream import ic
from scipy.io import loadmat, savemat

def add_pss(N_fft, cp): 
    """
    Добавление PSS 
    """
    #len_subcarr = len(self.activ_carriers(True))
        
    pss = zadoff_chu(PSS=True) #* 2**14 *3
    arr = np.zeros(N_fft, dtype=complex)

    # Массив с защитными поднесущими и 0 в центре
    arr[N_fft//2 - 31 : N_fft//2] = pss[:31]
    arr[N_fft//2 + 1: N_fft//2 + 32] = pss[31:]

    

    pss_time = np.fft.ifft(np.fft.fftshift(arr))
    pss_time_cp = np.concatenate([pss_time[-cp:], pss_time])
    return pss_time_cp


def corr_pss_time(rx, N_fft):
    

    pss = zadoff_chu(PSS = True)
        
    zeros = N_fft // 2 - 31
    pss_ifft = np.insert(pss, 32, 0)
    pss_ifft = np.insert(pss_ifft, 0, np.zeros(zeros))
    pss_ifft = np.append(pss_ifft, np.zeros(zeros-1))
        
    pss_ifft = np.fft.fftshift(pss_ifft)
    pss_ifft = np.fft.ifft(pss_ifft)
    #for i in range(len(rx) - 128):
        #o = corr_no_shift(rx[i : i+128], np.conjugate(pss_ifft), complex=True)
        #corr.append(abs(o))
    o = np.abs(np.convolve(np.flip(np.conjugate(pss_ifft)), rx, mode = "full"))


    indexes_max  =  o / np.max(o)#[i for i in range(len(o)) if o[i] > 100]    
    #cool_plot(indexes_max, title='corr_pss_time', show_plot=True)  
    plt.figure()
    plt.title("correlat norm")
    plt.plot(indexes_max)   

    indexes_max = [i for i in range(len(indexes_max)) if indexes_max[i] > 0.90]    
    #corr = np.array(corr) / np.max(corr)
        
        #maxi = np.argmax(corr)
        # for i in range(len(corr)):
        #     if corr[i] == 1:
        #         maxi = i
        #         break
        # maxi = maxi - 31 - cp-2
        # print('corr_pss_time',maxi)
        # from mylib import cool_plot
        # cool_plot(corr, title='corr_pss_time', show_plot=False)
    maxi = indexes_max[4]
    print("maxiiii", maxi)
        #rx = rx[maxi:maxi + (self.N_fft + self.CP_len) * 6]
    rx = rx[maxi:]
    return rx, maxi

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
                    if (i in range(GB, fft_len - GB - 1))
                    and (i != fft_len/2)
                ])
        else:
            activ = np.array([
                    i
                    for i in range(0, fft_len)
                    if (i in range(GB, fft_len - GB - 1))
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
    #ic(usable_bandwidth,pilot_spacing)
    # Можно менять значение от 0 до 1
    #                          ↓
    pilot_carriers = np.arange(0 + GB_len//2, N_fft - GB_len//2, pilot_spacing)
    #pilot_carriers = np.linspace(0 + self.GB_len//2, self.N_fft - self.GB_len//2+1, N_pil)

    for i in range(len(pilot_carriers)):
        if pilot_carriers[i] == 32:
            pilot_carriers[i] += 1
        
    # Handle potential rounding errors or edge cases
    if len(pilot_carriers) < N_pil:
        pilot_carriers = np.concatenate((pilot_carriers, [N_fft // 2 + 1]))  # Add center carrier if needed
    elif len(pilot_carriers) > N_pil:
        pilot_carriers = pilot_carriers[:N_pil]  # Truncate if there are too many
    
    pilot_carriers[-1] = N_fft - GB_len//2 - 2 # Последний пилот на последней доступной поднесущей
    
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


def modulation(N_fft, CP_len, QAM_sym,N_pilot, amplitude_all=2**14, amplitude_data=1, amplitude_pss=3, amplitude_pilots=3, ravel=True):
    """
    OFDM модуляция.

    Returns:
        np.ndarray: Массив OFDM-сигналов.
    """
    # Разделение массива symbols на матрицу(по n в строке)
    def reshape_symbols(symbols, activ):
        len_arr = len(activ)
        try:
            if (len(symbols) % len_arr) != 0:
                symbols1 = np.array_split(symbols[: -(len(symbols) % len_arr)], len(symbols) / len_arr)
                symbols2 = np.array((symbols[-(len(symbols) % len_arr) :]))
                
                ran_bits = randomDataGenerator((len_arr - len(symbols2))*2)
                zero_qpsk = list(QPSK(ran_bits, amplitude=1)) # 1+1j 
                
                zeros_last = np.array(zero_qpsk)
                symbols2 = np.concatenate((symbols2, zeros_last))
                symbols1.append(symbols2)
                symbols = symbols1
            else:
                symbols = np.array_split(symbols, len(symbols) / len_arr)
        except ValueError:
            zero = np.zeros(len_arr - len(symbols))
            symbols = np.concatenate((symbols, zero))
        
        return symbols

    def generate_pilot_symbol(n_pil):
        pilot = list(QPSK([0,0], amplitude=1)) 
        pilot_symbols = pilot * n_pil
        return np.array(pilot_symbols)


    def distrib_subcarriers(symbols, activ, fft_len, amplitude):
        len_symbols = np.shape(symbols)
        # Создание матрицы, в строчке по n символов QPSK
        if len(len_symbols) > 1: 
            arr_symols = np.zeros((len_symbols[0], fft_len), dtype=complex)
        else: # если данных только 1 OFDM символ
            arr_symols = np.zeros((1, fft_len), dtype=complex)
        
        # Распределение строк символов по OFDM символам(с GB и пилотами)
        pilot_carriers = generate_pilot_carriers(N_fft, GB_len, N_pilot)
        pilot_symbols = generate_pilot_symbol(N_pilot)
        for i, symbol in enumerate(arr_symols):
            index_pilot = 0
            index_sym = 0
            for j in range(len(symbol)):
                if j in pilot_carriers:
                    arr_symols[i][j] = pilot_symbols[index_pilot] * amplitude
                    index_pilot += 1
                elif (j in activ) and (index_sym < len_symbols[-1]):
                    if len(len_symbols) > 1:
                        arr_symols[i][j] = symbols[i][index_sym]
                    else:
                        arr_symols[i][j] = symbols[index_sym]
                    index_sym += 1
        
        return arr_symols

    def split_into_slots(symbols, chunk_size):
        chunks = []
        sym = list(symbols)
        # Разбивает `symbols` на фрагменты по `chunk_size`
        for i in range(0, len(sym), chunk_size):
            chunks.append(sym[i:i + chunk_size])
        return chunks

    def to_binary_fixed_length(number, length=8):
        binary_array = []
        for i in range(length):
            bit = number & (1 << (length - i - 1))
            binary_array.append(bit >> (length - i - 1))
        return binary_array

    def add_pss(fft_len, symbols, amplitude): 
        """
        Добавление PSS 
        
        Работает правильно
        """
        #len_subcarr = len(self.activ_carriers(True))
        
        pss = zadoff_chu(PSS=True) * amplitude
        arr = np.zeros(fft_len, dtype=complex)

        # Массив с защитными поднесущими и 0 в центре
        arr[fft_len//2 - 31 : fft_len//2] = pss[:31]
        arr[fft_len//2 + 1: fft_len//2 + 32] = pss[31:]
        
        symbols = np.insert(symbols, 0, arr, axis=0)
        
        for i in range(6, symbols.shape[0], 6):
            symbols = np.insert(symbols, i, arr, axis=0)

        return symbols

    def add_CRC(slot_pre_post):
        print(len(slot_pre_post))
        data = QPSK(slot_pre_post, amplitude=1) # Демодуляция по QPSK
        data = list(data)
        G = [1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1,1] # полином для вычисления crc

        data_crc = data + 16 * [0]
        for i in range(0,len(data_crc)-16):
            if(data_crc[i] == 1):
                for j in range(len(G)):
                    data_crc[i+j] = data_crc[i+j] ^ G[j]
        crc = data_crc[len(data_crc)-16:]

        return np.array(crc)

    fft_len = N_fft
    _cyclic_prefix_len = CP_len
    _guard_band_len = GB_len
    symbols = QAM_sym
    pilot_carrier = generate_pilot_carriers(N_fft, GB_len, N_pilot)
    activ = activ_carriers(N_fft, GB_len, pilot_carrier, pilots = False)
    print("len active carr = ", len(activ))
    len_prefix_max_slots = int(np.log2(256))

    # Нормирование амплитуд
    am_max = np.max([amplitude_data, amplitude_pilots, amplitude_pss])
    amplitude_data = amplitude_data / am_max
    amplitude_pilots = amplitude_pilots / am_max
    amplitude_pss = amplitude_pss / am_max
        
    symbols = split_into_slots(symbols, (-len_prefix_max_slots -4 +(len(activ))*5) -8)
    
    # Делим массив символов на матрицу (в строке элеметнов = доступных поднесущих)
    slots = []
    for slot, i in zip(symbols, range(len(symbols))):
        # Заполнение префикса
        slot_number = QPSK(to_binary_fixed_length(i+1, len_prefix_max_slots), amplitude=1)
        total_slots = QPSK(to_binary_fixed_length(len(symbols), len_prefix_max_slots), amplitude=1)
        useful_bits = QPSK(to_binary_fixed_length(len(slot)+8+4+8, 8), amplitude=1)
        
        slot_pre_post  = np.concatenate((slot_number, total_slots, useful_bits, slot))
        # CRC
        crc = QPSK(add_CRC(slot_pre_post), amplitude=1) 
        
        slot_pre_post  = np.concatenate((slot_pre_post, crc))
        
        
        slot_pre_post = reshape_symbols(slot_pre_post, activ) 

        ran_bits = randomDataGenerator(len(activ)*2)
        zero_qpsk = list(QPSK(ran_bits, amplitude=1)) # 1+1j 
        
        # Добавление недостающих OFDM символов для заполнения слота
        empty_symbol = []
        for em in range(0, 5 - np.shape(slot_pre_post)[0]):
            empty_symbol.append(zero_qpsk)
        if len(empty_symbol) > 0:
            slot_pre_post = np.concatenate((slot_pre_post, empty_symbol))
        
        #ic(np.shape(slot_pre_post))
        slots.append(slot_pre_post)
    
    slots = np.concatenate(slots, axis=0)
    
    print("len slots",len(slot))

    slots = slots * amplitude_data
    arr_symols = distrib_subcarriers(slots, activ, fft_len, amplitude_pilots)
    arr_symols = add_pss(fft_len, arr_symols, amplitude_pss)
    
    arr_symols = np.fft.fftshift(arr_symols, axes=1)
    print("len sym =",len(arr_symols[23]))
    # IFFT
    ifft = np.zeros((np.shape(arr_symols)[0], fft_len), dtype=complex)
    for i in range(len(arr_symols)):
        ifft[i] = np.fft.ifft(arr_symols[i])
    
    # Добавление циклического префикса
    fft_cp = np.zeros((np.shape(arr_symols)[0], (fft_len + _cyclic_prefix_len)), dtype=complex)
    for i in range(np.shape(arr_symols)[0]):
        fft_cp[i] = np.concatenate((ifft[i][-_cyclic_prefix_len:], ifft[i]))
    
    fft_cp = fft_cp * amplitude_all
    ic(len(fft_cp[0]))
    if ravel:
        return np.ravel(fft_cp)
    return fft_cp


def OFDM_MOD(N_fft, GB_len, N_pil, QAM , CP, ampl = 2**14): # формирование OFDM символы
    
    pilot = complex(0.7,0.7) 

    len_data = N_fft-N_pil-GB_len

    pilot_carrier = generate_pilot_carriers(N_fft, GB_len, N_pil)
    ic(pilot_carrier)
    data_carrier = activ_carriers(num_carrier, GB_len, pilot_carrier)
    print("len data=",len(data_carrier))
    count_ofdm_symbol = len(QAM) // len(data_carrier) + 1 
    ofdm = np.zeros((count_ofdm_symbol, N_fft),dtype=np.complex128)
    pss = add_pss(num_carrier,CP)*2
    
    ofdm_ifft_cp = np.zeros(0)
    for j in range(count_ofdm_symbol):
            if j % 6 != 0:
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
            else:
                ofdm_ifft_cp = np.concatenate([ofdm_ifft_cp, pss])
    
    
    #ofdm_ifft_cp_pss = np.concatenate([pss, ofdm_ifft_cp]) 
    ofdm_ifft_cp *= ampl
    return ofdm_ifft_cp

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
        if corr_sum > max and corr_sum > 0.98:
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

def interpolatin_pilot(pilot_carrier, rx_sync,GB_len):
    rx = np.asarray(rx_sync)
    #Hls = rx[0][index_pilot]
    
    for i in range(len(pilot_carrier)):
        if pilot_carrier[i] >  128//2:
            pilot_carrier[i] -= 1
    pilot_carrier = pilot_carrier-(GB_len//2  ) 
    print("pppp",pilot_carrier)    

    rx_pilot = np.array([np.take(row, pilot_carrier) for row in rx])
    print("pilot int1",pilot_carrier)
    count_ofdm = len(rx_sync)
    num_carrier = len(rx_sync[0])
    
    pilot = complex(1,1) 
    Hls = rx_pilot / pilot                                                    # частотная характеристика канала на пилотах

    Hls1 = Hls.flatten()

    if 0:                                                                    
        plt.figure(7)
        plt.title("Частотная характеристика канала на пилотах")
        plt.stem(abs(Hls1), "r",label='pilot - ampl')
        plt.stem(np.angle(Hls1),label='pilot - phase')
        plt.legend(loc='upper right')

                                                   # индексы пилотов без защитных нулей

    #print(Hls)

    all_inter = np.zeros(0)

    ### Интерполяция ###
    for i in  range(count_ofdm):                                               # цикл по количеству ofdm символов
        x_interp = np.linspace(pilot_carrier[0], pilot_carrier[-1], num_carrier)#np.linspace(0, num_carrier, num_carrier)

        #print("pilot val = ", Hls[i])
        interpol = np.interp(x_interp, pilot_carrier, Hls[i])
        #print("interpol = ", interpol)

        
        all_inter = np.concatenate([all_inter, interpol])


    #print(all_inter)
    #interpol = y_interp
    #print("len inter",len(interpol))
    #interpol = interpol.flatten()
    if 1:
        plt.figure(8)
        plt.title('Интерполяция')
        plt.stem(abs(all_inter))
        plt.show()
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


def calculate_correlation(pss, matrix_name, m):
  """
  Calculates correlation between pss and matrix_name with filtering and delay.

  Args:
      pss: The reference signal.
      matrix_name: The signal to compare with pss.
      m: Decimation factor.

  Returns:
      A tuple containing the correlation and carrier frequency offset (CFO).
  """
  L = len(pss)

  # Flipped and complex conjugated reference signal
  corr_coef = np.flip(np.conjugate(pss))

  # Filter reference signal sections
  partA = np.convolve(corr_coef[:L // 2], matrix_name, mode='full')
  xDelayed = np.concatenate((np.zeros(L // 2), matrix_name[:-L // 2]))
  partB = np.convolve(corr_coef[L // 2:], xDelayed, mode='full')

  # Calculate correlation and phase difference
  correlation = np.abs(partA + partB)
  phaseDiff = partA * np.conj(partB)

  # Find maximum correlation and corresponding phase difference
  istart = np.argmax(correlation)
  phaseDiff_max = phaseDiff[istart]

  # Calculate CFO
  CFO = np.angle(phaseDiff_max) / (np.pi * 1 / m)
  t = np.arange(0,len(matrix_name))
  t = t / 1920000

 
  data_offset = matrix_name * np.exp(-1j * 2 * np.pi * np.conjugate(CFO) * t)

  return data_offset


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



def indexs_of_CP_after_PSS(rx, cp, fft_len):
    """
    Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
    """
    corr = [] # Массив корреляции 

    for i in range(len(rx) - fft_len):
        o = norm_corr((rx[:cp]), rx[fft_len:fft_len+cp])

        corr.append(abs(o))
        rx = np.roll(rx, -1)

    corr = np.array(corr) / np.max(corr) # Нормирование
    max_len_cycle = len(corr)
    # if corr[0] > 0.97:
    #     max_len_cycle = len(corr)
    # else:
    #     max_len_cycle = len(corr)-(fft_len+cp)

    ind = np.argmax(corr[0 : (fft_len+cp)// 2 ])
    arr_index = [] # Массив индексов максимальных значений corr
    arr_index.append(ind)
    for i in range((fft_len+cp) // 2, max_len_cycle, (fft_len+cp)):
        #print(i, i+(fft_len+cp))
        max = np.max(corr[i : i+(fft_len+cp)])
        if max > 0.90: 
            ind = i + np.argmax(corr[i : i+(fft_len+cp)])
            if ind < (len(corr)):
                arr_index.append(ind)
    
    ### DEBUG
    
    # print(corr)
    plt.figure()
    plt.plot(abs(corr))
    plt.show()
    return arr_index


def indiv_symbols(ofdm, N_fft, CP_len):
    cp = CP_len
    all_sym = N_fft + cp
    
    
    index = indexs_of_CP_after_PSS(ofdm, cp, N_fft)
    
    symbols = []
    for ind in index:
        symbols.append(ofdm[ind+cp : ind+all_sym])
        
    return np.asarray(symbols)


def resource_grid_3(data1, Nfft, cp): 
    """
        data - matrix
        count_frame - количество OFDM фреймов бля ресурсной сетки
        len_frame - количество ofdm-символов в ofdm фрейме
        Nftt - количество поднесущих
        cp - защитный префикс

    """
    #data1 = data[:(Nfft)*len_frame*count_frames]
    half_nfft = Nfft//2

    # преобразуем в матрицу 
    data_freq = data1.reshape(len(data1)//(Nfft+cp), (Nfft+cp))

    # обрезаем циклический префикс
    data1 = data_freq[:, cp:]
    # производим обратное преобразование фурье и транспонируем матрицу для удобного вывода на карте

    data2 = np.fft.fft(data1).T

    # переставляем строки местами из-за не шифтнутых частот
    temp = np.copy(data2[0:half_nfft, :])
    data2[0:half_nfft, :] = data2[half_nfft:Nfft, :]
    data2[half_nfft:Nfft, :] = temp

    plt.figure()
    plt.imshow(abs(data2), cmap='jet',interpolation='nearest', aspect='auto')
    plt.colorbar()
    plt.show()

def fft(num_carrier,GB_len, ofdm_symbols, pilot_carrier, ravel = True, GB = False, pilots = True):
    fft = []
    len_c = np.shape(ofdm_symbols)[0]
    for i in range(len_c):
        if len_c == 1:
            zn = np.fft.fftshift(np.fft.fft(ofdm_symbols))
        else:
            zn = np.fft.fftshift(np.fft.fft(ofdm_symbols[i]))
            
        if (GB is False) and (pilots is False):
            zn = zn[activ_carriers(num_carrier, GB_len, pilot_carrier, pilots = False)]
        elif (GB is True):
            pass
        else:
            zn = zn[activ_carriers(num_carrier, GB_len, pilot_carrier, pilots = True)]
            
        fft.append(zn)
            
    if ravel:
        ret = np.ravel(fft)
        return ret
    else:
        return fft

def resource_grid_2(data, Nfft): 
    """
        data - matrix
        count_frame - количество OFDM фреймов бля ресурсной сетки
        len_frame - количество ofdm-символов в ofdm фрейме
        Nftt - количество поднесущих
        cp - защитный префикс

    """
    #data1 = data[:(Nfft)*len_frame*count_frames]
    half_nfft = Nfft//2

    # преобразуем в матрицу 
    #data_freq = data1.reshape(len_frame*count_frames, (Nfft+cp))

    # обрезаем циклический префикс
    #data1 = data_freq[:, cp:]
    # производим обратное преобразование фурье и транспонируем матрицу для удобного вывода на карте

    data2 = np.fft.fft(data).T

    # переставляем строки местами из-за не шифтнутых частот
    temp = np.copy(data2[0:half_nfft, :])
    data2[0:half_nfft, :] = data2[half_nfft:Nfft, :]
    data2[half_nfft:Nfft, :] = temp

    plt.figure()
    plt.imshow(abs(data2), cmap='jet',interpolation='nearest', aspect='auto')
    plt.colorbar()
    plt.show()




        

#sdr = standart_settings("ip:192.168.2.1", 1.920e6, 10e3)
#sdr2 = standart_settings("ip:192.168.3.1", 1.920e6, 10e3)

num_carrier = 128

N_pilot = 6
GB_len = 55
CP = 32

mes = "lalalavavavavavfjkafbaldj123456781lalalavavavavavsdfghjkjhgfdfghj" #2 ofdm 
mes2 = "A small sfsdfsdfsf"
bit = randomDataGenerator(2000)
bit1 = text_to_bits(mes)


qpsk1 = QPSK(bit)
len_qpsk = len(qpsk1)
print(len_qpsk)



#pilot_carrier = generate_pilot_carriers(num_carrier, GB_len, N_pilot)
#data_carrier = activ_carriers(num_carrier, GB_len, pilot_carrier)
#print(pilot_carrier)
#print(data_carrier)

#ofdm = OFDM_MOD(num_carrier, GB_len, N_pilot, qpsk1, CP, ampl = 2**15)
ofdm = modulation(num_carrier, CP,qpsk1, N_pilot, amplitude_all= 2**14, amplitude_pss = 1, amplitude_pilots = 1)
print('dfgnmgfdfghj',len(ofdm))
resource_grid_3(ofdm, num_carrier,CP)


#tx_signal(sdr,1900e6,0,ofdm)
#rx_sig = rx_signal(sdr2,1900e6,20,3)


#rxMax = max(rx_sig.real)
#rx_sig = rx_sig / rxMax
if 0:
    rx_sig =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\rx_before_2_sdr1.mat")



    h1 = list(rx_sig.values())
    rx_sig = np.asarray(h1[3])
    rx_sig = np.ravel(rx_sig)

    pss =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\pss_time.mat")

    h = list(pss.values())
    pss = np.asarray(h[3])
    pss = np.ravel(pss)


    plt.figure()
    plt.plot(20*np.log10(abs(np.fft.fft(rx_sig))))

    rx_ofdm, maxi = corr_pss_time(rx_sig,num_carrier)

    plot_QAM(rx_ofdm)

    #resource_grid(rx_ofdm,10,4,num_carrier, CP)

    data = calculate_correlation(pss, rx_ofdm, 15000)

    resource_grid(data,10,6,num_carrier, CP)


    #data = data[:((num_carrier + CP) * 5)]


    data = indiv_symbols(data, num_carrier, CP)
    data = data[:4,:]
    resource_grid_2(data,num_carrier)
    #index = correlat_ofdm(rx_sig,CP,num_carrier)
    #index = correlate_frame(rx_sig, len(pss), len_pack)

    #rx_ofdm = rx_sig[index:]
    #rx_ofdm = rx_sig[len(pss):]
    #rx_ofdm = rx_ofdm[:len(ofdm)]

    #ofdm2 = rx_ofdm.reshape(len(rx_ofdm)//(num_carrier+CP),num_carrier+CP)

    #rx_ofdm = Freq_Correction(ofdm2, num_carrier, CP)

    #data = data.flatten()


    #del_cp = delete_CP(data, num_carrier, CP)
    data = fft(num_carrier, GB_len, data, pilot_carrier)
    print("data len = ",len(data))


    ofdm1 = data #del_cp.reshape(len(del_cp)//num_carrier,num_carrier)

    #ofdm1 = Classen_Freq(ofdm1,num_carrier,pilot, pilot_carrier)

    #del_cp = ofdm1.flatten()
    #plot_QAM(del_cp, "Befor Interpolation")



    #ofdm1 = Classen_Freq(ofdm1,num_carrier,pilot, pilot_carrier)
    ofdm1 = data.reshape(len(data)//(num_carrier-GB_len+1),(num_carrier-GB_len+1))
    #print(ofdm1)
    #value_pilot = get_value_pilot(ofdm1,pilot_carrier)
    inter = interpolatin_pilot(pilot_carrier, ofdm1, GB_len)

    #inter = interpol_pilots(rx_ofdm, num_carrier,GB_len, pilot_carrier, CP)

    #plt.figure(2)
    #plot_QAM(inter, "AFTER Interpolation")


    #plt.figure(1)
    #plt.plot(abs(np.fft.fft(ofdm)))
    print("pilot carrier = ",pilot_carrier)
    data_carrier1 = activ_carriers(num_carrier, GB_len, pilot_carrier, pilots = True)
    print("data car 1 = ",data_carrier1)

    for i in range(len(data_carrier1)):
        if data_carrier1[i] > num_carrier//2:
            data_carrier1[i] -=1
    data_carrier1 -= GB_len//2

    print("ll",data_carrier1, len(data_carrier1))
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

    ofdm2 = data_pilot.reshape(len(data_pilot)//(num_carrier-GB_len+1),num_carrier-GB_len+1)

    print("oly_pilot: ",pilot_carrier-GB_len//2)

    #print("ofdm2 = ", len(ofdm2),len(ofdm2[0]), ofdm2)

    data = np.zeros(0)
    for i in range(len(ofdm2)):
            #print(i)
            qpsk = ofdm2[i][data_carrier1_not_pilot]
            data = np.concatenate([data, qpsk])



    #data = data[abs(data) >= 0.5] # удаление нулей из последнего ofdm


    plot_QAM(data, "qpsk")



    deqpsk = DeQPSK(data)
    text = bits_array_to_text(deqpsk)
    print(text)
    plt.show()



