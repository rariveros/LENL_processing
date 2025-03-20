from directories import *
from back_process import *

if __name__ == '__main__':

    def biGauss(x, AL, AR, x0L, x0R, sigmaL, sigmaR):
        return np.abs(AL * np.exp(-(x - x0L) ** 2 / (2 * sigmaL ** 2)) - AR * np.exp(-(x - x0R) ** 2 / (2 * sigmaR ** 2)))

    def Gauss(x, A, x0, sigma):
        return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

    ###    Abriendo archivos    ###
    disco = 'D:'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data/soliton_control/espacio_parametros/a=1_f=13.7'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_strobo.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    Z_mean = np.mean(Z, axis=0)

    parameters, covariance = curve_fit(biGauss, X, Z_mean, bounds=([0.4, 0.4, 10, -30, 1, 1], [0.6, 0.6, 30, -10, 20, 20]))
    print(parameters)
    AL, AR, x0L, x0R, sigmaL, sigmaR = parameters
    fit_y = biGauss(X, AL, AR, x0L, x0R, sigmaL, sigmaR)
    plt.plot(X, Z_mean, color="k", label='EXP', lw=3)
    plt.plot(X, Gauss(X, AL, x0L, sigmaL), color="r", ls="--", label='fit', lw=2)
    plt.plot(X, Gauss(X, AR, x0R, sigmaR), color="r", ls="--", label='fit', lw=2)
    plt.plot(X, fit_y, '-', color="r", label='fit', lw=2)
    plt.legend()
    plt.show()