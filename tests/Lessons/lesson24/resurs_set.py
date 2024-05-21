import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat

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



def norm_corr(x,y):
    #x_normalized = (cp1 - np.mean(cp1)) / np.std(cp1)
    #y_normalized = (cp2 - np.mean(cp2)) / np.std(cp2)

    c_real = np.vdot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
    c_imag = np.vdot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
    
    return c_real+1j*c_imag

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
    print(arr_index)
    # print(corr)
    plt.figure()
    plt.plot(abs(corr))
    plt.show()
    return arr_index

def indiv_symbols(ofdm, N_fft, CP_len):
    cp = CP_len
    all_sym = N_fft + cp
    
    
    index = indexs_of_CP_after_PSS(ofdm, cp, N_fft)

    ic(index)
    #ofdm = self.freq_syn(ofdm, index)
    
    symbols = []
    for ind in index:
        symbols.append(ofdm[ind : ind+all_sym])
        
    return np.asarray(symbols)

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
    plt.show()  

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
    maxi = indexes_max[1]
    print("maxiiii", maxi)
        #rx = rx[maxi:maxi + (self.N_fft + self.CP_len) * 6]
    rx = rx[maxi:]
    return rx

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


def resource_grid(data, count_frames, len_frame, Nfft, cp ): 
    """
        data - данные для ресурсной сетки 
        count_frame - количество OFDM фреймов бля ресурсной сетки
        len_frame - количество ofdm-символов в ofdm фрейме
        Nftt - количество поднесущих
        cp - защитный префикс

    """
    data = data[:(Nfft+cp)*len_frame*count_frames]
    half_nfft = Nfft//2

    # преобразуем в матрицу 
    data_freq = data.reshape(len_frame*count_frames, (Nfft+cp))

    # обрезаем циклический префикс
    data1 = data_freq[:, cp:]
    # производим обратное преобразование фурье и транспонируем матрицу для удобного вывода на карте
    data2 = np.fft.fft(data1).T

    # переставляем строки местами из-за не шифтнутых частот
    temp = np.copy(data2[0:half_nfft, :])
    data2[0:half_nfft, :] = data2[half_nfft:Nfft, :]
    data2[half_nfft:Nfft, :] = temp

    
    plt.imshow(abs(data2), cmap='jet',interpolation='nearest', aspect='auto')
    plt.colorbar()
    plt.show()

data =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\rx_before_2_sdr.mat")
pss =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\pss_time.mat")

h = list(pss.values())
pss = np.asarray(h[3])
pss = np.ravel(pss)

h1 = list(data.values())
data = np.asarray(h1[3])
data = np.ravel(data)

frame = 10


num_carrier = 128
GB_len = 55
CP_len = 32


data = corr_pss_time(data, 128)

resource_grid(data, 20, 6, 128,32)

data_freq = calculate_correlation(pss, data, 15000)
# test =  loadmat("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson23\\freq.mat")
# h2 = list(test.values())
# test = np.asarray(h2[3])
# test = np.ravel(test)

# test = test[:960*frame]
resource_grid(data_freq, 20, 6, 128,32)


