import numpy as np
import matplotlib.pyplot as plt



def generate_sig(A, frequency, T, size): # для формирования графиков с верным кол-вом отчетов
    t = np.linspace(0, 1, size)
    x = A * np.cos(2 * np.pi * frequency * t)
    return x

def generate_sig_spectrum(A, frequency, T, size): #для формирования графиков с верным спектром
    t = np.linspace(0, (size-1)*T, size)
    x = A * np.cos(2 * np.pi * frequency * t)
    return x

A = 2     
f = 10      
fs = 100    
T = 1/fs   

sample_64 = 64
sample_128 = 128
sample_256 = 256


def disc_samp():                            # 2.1 Вывод графиков с разным кол-вом отсчетов
    x1 = generate_sig(A, f, T, sample_64)
    t = np.linspace(0, 1, sample_64)
    x2 = generate_sig(A, f, T, sample_128)
    t2 = np.linspace(0, 1, sample_128)
    x3 = generate_sig(A, f, T, sample_256)
    t3 = np.linspace(0, 1, sample_256)


    plt.subplot(3,1,1)
    plt.title('64 отсчета')
   # plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.stem(t,x1)
    plt.subplot(3,1,2)
    plt.title('128 отсчета')
    #plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.stem(t2,x2)
    plt.subplot(3,1,3)
    plt.title('256 отсчета')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.stem(t3,x3)
    

    plt.show()



def spectrum():                                    # 2.3 вычисление ДПФ сигнала из раздела 1 для трех наборов отсчетов

    x = generate_sig_spectrum(A, f, T, sample_64)
    t = np.linspace(0, (sample_64-1)*T, sample_64)
    x2 = generate_sig_spectrum(A, f, T, sample_128)
    t2 = np.linspace(0, (sample_128-1)*T, sample_128)
    x3 = generate_sig_spectrum(A, f, T, sample_256)
    t3 = np.linspace(0, (sample_256-1)*T, sample_256)
    X = np.fft.fft(x)
    X2 = np.fft.fft(x2)
    X3 = np.fft.fft(x3)

    freq1 = np.fft.fftfreq(sample_64, d=T)
    freq2 = np.fft.fftfreq(sample_128, d=T) 
    freq3 = np.fft.fftfreq(sample_256, d=T) 
    plt.subplot(3,1,1)
    plt.xlabel('Частота, Гц')
    plt.ylabel('Модуль спектра')
    plt.stem(freq1, np.abs(X))
    plt.subplot(3,1,2)
    plt.xlabel('Частота, Гц')
    plt.ylabel('Модуль спектра')
    plt.stem(freq2, np.abs(X2))
    plt.subplot(3,1,3)
    plt.stem(freq3, np.abs(X3))
    plt.xlabel('Частота, Гц')
    plt.ylabel('Модуль спектра')
    plt.show()

def norm_freq():                   # 2.2 Значение аналоговой частоты сигнала, которая соответствует нормированной частоте
    #f_n = 2*np.pi*f/fs 
    
    freq_analog1 = (0.1*fs)/2
    freq_analog2 = (0.3*fs)/2
    print('Аналоговая частота при нормированной частоте Ω=0.1π freq_analog1=', freq_analog1)
    print('Аналоговая частота при нормированной частоте Ω=0.3π freq_analog2=', freq_analog2)

disc_samp()
norm_freq()
spectrum()