'''
Модуль "Plots"

1) plot_QAM() 
    - предназназначен для быстрой отрисовки map QAM
    - на вход подается numpy array комплексных чисел
'''
import matplotlib.pyplot as plt

def plot_QAM(a, title = "qam"):
    plt.title(title)
    plt.grid(0)
    plt.axhline(y=0,color = 'red')
    plt.axvline(x=0,color = 'red')
    colors = range(len(a))
    plt.scatter(a.real, a.imag, s=5, c=colors, cmap="prism", alpha=1)
    plt.xlabel("real")
    plt.ylabel("imag")
    #plt.show()



def drav_plot():
    pass