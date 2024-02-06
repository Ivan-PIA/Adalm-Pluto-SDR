import matplotlib.pyplot as plt
import numpy as np



def plot_QAM(a):
    plt.title("test")
    plt.grid()
    plt.axhline(y=0,color = 'red')
    plt.axvline(x=0,color = 'red')
    plt.scatter(a.real, a.imag)
    plt.show()



def drav_plot():
    pass