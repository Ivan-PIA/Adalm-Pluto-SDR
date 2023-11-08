import numpy as np
import matplotlib.pyplot as plt



def generate_sig(A, frequency, T, size):
    t = np.linspace(0, (size-1)*T, size)
    x = A * np.cos(2 * np.pi * frequency * t)
    return x

A = 2       # Амплитуда
f = 10       # Частота сигнала, Гц
fs = 20    # Частота дискретизации, отсч/сек
T = 1/fs    # Интервал времени

sample_64 = 64
sample_128 = 128
sample_256 = 256

def disc_samp():
    x1 = generate_sig(A, f, T, sample_64)
    t = np.linspace(0, (sample_64-1)*T, sample_64)
    x2 = generate_sig(A, f, T, sample_128)
    t2 = np.linspace(0, (sample_128-1)*T, sample_128)
    x3 = generate_sig(A, f, T, sample_256)
    t3 = np.linspace(0, (sample_256-1)*T, sample_256)
    plt.subplot(3,1,1)
    plt.stem(t,x1)
    plt.subplot(3,1,2)
    plt.stem(t2,x2)
    plt.subplot(3,1,3)
    plt.stem(t3,x3)

    plt.show()

disc_samp()

def spectrum():

    x = generate_sig(A, f, T, sample_64)
    t = np.linspace(0, (sample_64-1)*T, sample_64)
    x2 = generate_sig(A, f, T, sample_128)
    t2 = np.linspace(0, (sample_128-1)*T, sample_128)
    x3 = generate_sig(A, f, T, sample_256)
    t3 = np.linspace(0, (sample_256-1)*T, sample_256)
    X = np.fft.fft(x)
    X2 = np.fft.fft(x2)
    X3 = np.fft.fft(x3)

    freq1 = np.fft.fftfreq(sample_64, d=T)
    freq2 = np.fft.fftfreq(sample_128, d=T) 
    freq3 = np.fft.fftfreq(sample_256, d=T) 
    plt.subplot(3,1,1)
    plt.stem(freq1, np.abs(X))
    plt.subplot(3,1,2)
    plt.stem(freq2, np.abs(X2))
    plt.subplot(3,1,3)
    plt.stem(freq3, np.abs(X3))
    plt.xlabel('Частота, Гц')
    plt.ylabel('Модуль спектра')
    plt.show()

spectrum()