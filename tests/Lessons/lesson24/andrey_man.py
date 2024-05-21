import numpy as np
import matplotlib.pyplot as plt

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
    data_freq = data1.reshape(2, (Nfft+cp))

    # обрезаем циклический префикс
    data1 = data_freq[:, cp:]
    # производим обратное преобразование фурье и транспонируем матрицу для удобного вывода на карте

    data2 = np.fft.fft(data1).T

    # переставляем строки местами из-за не шифтнутых частот
    #temp = np.copy(data2[0:half_nfft, :])
    #data2[0:half_nfft, :] = data2[half_nfft:Nfft, :]
    #data2[half_nfft:Nfft, :] = temp

    plt.figure()
    plt.imshow(abs(data2), cmap='jet',interpolation='nearest', aspect='auto')
    plt.colorbar()
    plt.show()


array = np.loadtxt('C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson24\\dla_ivana2.txt').view(complex)


print(array)

print(len(array))

cp = 16
nfft = 64

resource_grid_3(array,nfft,cp)