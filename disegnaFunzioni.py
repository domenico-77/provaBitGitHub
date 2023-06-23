import numpy as np
import matplotlib.pyplot as plt

def plot_vertical_line(x):
    plt.axvline(x=x, color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Grafico della linea verticale')
    plt.grid(True)
    plt.show()

def plot_horizontal_line(y):
    plt.axhline(y=y, color='blue')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Grafico della linea verticale')
    plt.grid(True)
    plt.show()

def plot_horizontal_and_vertical_line(x, y):
    plt.axvline(x=x, color='red')
    plt.axhline(y=y, color='blue')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Grafico delle linee')
    plt.grid(True)
    plt.show()


def plot_function(func, x_start, x_end, step=0.1):
    x = np.arange(x_start, x_end, step)
    y = func(x)

    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Grafico della funzione')
    plt.grid(True)
    plt.show()

# Esempio di funzione: f(x) = x^2
def square_function(x):
    return x**2





x = 10
#plot_vertical_line(x)
#plot_horizontal_line(x)
plot_horizontal_and_vertical_line(x, x) #esperimento per plottare più linee
#plot_function(square_function, -5, 5)

