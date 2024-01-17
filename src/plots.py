import matplotlib.pyplot as plt
import numpy as np



def plot(a,b):
    plt.title("lox")
    plt.grid()
    plt.axhline(y=0,color = 'red')
    plt.axvline(x=0,color = 'red')
    plt.plot(a,b)
    plt.show()