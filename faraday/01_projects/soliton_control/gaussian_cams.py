from directories import *
from back_process import *
from back_faraday import *


if __name__ == "__main__":

    ang = 15
    ang_rad = (2 * np.pi / 360) * 8
    m_1 = 6 / np.pi
    m_2 = 12 / np.pi
    m_3 = 15 / np.pi
    A = m_3 * ang_rad
    sigma = 60

    f_0 = 0
    f_1 = m_1 * ang_rad
    f_2 = m_2 * ang_rad
    f_3 = m_3 * ang_rad

    x_grid = 18.5 * np.arange(0, 13)
    x_grid = x_grid - x_grid[-1] / 2
    x_grid_dense = 18.5 * np.arange(0, 13, 0.01)
    x_grid_dense = x_grid_dense - x_grid_dense[-1] / 2

    F_gaussian = A * np.exp(- x_grid ** 2 / (2 * sigma ** 2))
    Gaussian_dense = A * np.exp(-x_grid_dense ** 2 / (2 * sigma ** 2))
    levels = [f_0, f_1, f_2, f_3]

    fitted_levels = []
    for i in range(len(F_gaussian)):
        diff = []
        for j in range(len(levels)):
            diff_j = np.abs(F_gaussian[i] - levels[j])
            diff.append(diff_j)
        diff_min = min(diff)
        index_min = diff.index(diff_min)
        fitted_levels_i = levels[int(index_min)]
        fitted_levels.append(fitted_levels_i)

    plt.plot(x_grid_dense,Gaussian_dense, color="r")
    plt.scatter(x_grid, fitted_levels)
    plt.show()
    plt.close()





























