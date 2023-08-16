from directories import *
from back_process import *
from itertools import zip_longest


if __name__ == "__main__":
    x_grid = np.arange(0, 10, 0.01)
    a = 2
    b = 3
    c = 5
    y = a * x_grid ** 2 + b * x_grid + c
    ajuste = np.polyfit(x_grid, y, 2)
    print(ajuste)
    centro = - 2 * ajuste[1] / ajuste[0]
    print(centro, - 2 * b / a)
