from directories import *
from back_process import *

if __name__ == "__main__":
    t_grid = np.arange(0, 100, 0.01)
    w = 2 * np.pi * 1
    x_grid = np.sin(w * t_grid)
    sigma = np.std(x_grid)
    print(sigma * np.sqrt(2))