'''
Модуль "Plots"

1) plot_QAM() 
    - предназназначен для быстрой отрисовки map QAM
    - на вход подается numpy array комплексных чисел
'''
import matplotlib.pyplot as plt

def plot_QAM(a):
    plt.title("test")
    plt.grid()
    plt.axhline(y=0,color = 'red')
    plt.axvline(x=0,color = 'red')
    plt.scatter(a.real, a.imag)
    plt.show()



def drav_plot():
    pass