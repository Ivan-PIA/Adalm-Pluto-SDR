'''
Модуль "Plots"

1) plot_QAM() 
    - предназназначен для быстрой отрисовки map QAM
    - на вход подается numpy array комплексных чисел
'''
import matplotlib.pyplot as plt
import numpy as np

def plot_QAM(a, title = "qam"):
    plt.figure(figsize=(6,6))
    plt.title(title)
    plt.grid(0)
    plt.axhline(y=0,color = 'red')
    plt.axvline(x=0,color = 'red')
    colors = range(len(a))
    plt.scatter(a.real, a.imag, s=5, c=colors, cmap="prism", alpha=1)
    plt.xlabel("real")
    plt.ylabel("imag")
    #plt.show()



def resource_grid(data, count_frames, len_frame, Nfft, cp ): 
    """
        data - данные для ресурсной сетки 
        count_frame - количество OFDM фреймов бля ресурсной сетки
        len_frame - количество ofdm-символов в ofdm фрейме
        Nftt - количество поднесущих
        cp - защитный префикс

    """
    data1 = data[:(Nfft+cp)*len_frame*count_frames]
    half_nfft = Nfft//2

    # преобразуем в матрицу 
    data_freq = data1.reshape(len_frame*count_frames, (Nfft+cp))

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