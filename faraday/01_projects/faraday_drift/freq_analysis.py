from back_process import *
from numpy import genfromtxt
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':

    ###   OPEN FILES   ###
    print('Abriendo archivos...')
    datos_path = 'E:\mnustes_science\experimental_data'
    carpeta = select_directory(datos_path)
    x = []
    y = []
    y_err = []

    onlyfiles = [f for f in listdir(carpeta) if isfile(join(carpeta, f))]
    for i in range(len(onlyfiles)):
        current_csv = carpeta + '/' + onlyfiles[i]
        info_dvelocity = genfromtxt(current_csv, delimiter=',')
        ampd = info_dvelocity[0, 0]
        Gamma = (((14.8 / 2) / (2 * np.pi)) ** 2) * (ampd / 12) * 0.5
        mean = np.mean(info_dvelocity[:, 4])
        std = np.std(info_dvelocity[:, 4])
        x.append(Gamma)
        y.append(mean)
        y_err.append(std)
    x_np = np.array(x)
    y_np = np.array(y)
    yerr_np = np.array(y_err)


    def linear_fit(x, m, n):
        return m * x + n


    popt, pcov = curve_fit(linear_fit, x_np, y_np)
    m = popt[0]
    n = popt[1]

    print(m)
    print(n)

    x_grid = np.arange(x[0] - (x[0] - x[1]) / 2, x[-1] + (x[0] - x[1]) / 2, 0.01)
    y_grid = m * x_grid + n

    np.savetxt(carpeta + '/freq_processed/gammas.csv', x_np, delimiter='.')
    np.savetxt(carpeta + '/freq_processed//freq_k.csv', y_np, delimiter='.')
    np.savetxt(carpeta + '/freq_processed//freq_err.csv', yerr_np, delimiter='.')

    plt.grid()
    plt.xlim([x[0] - (x[0] - x[1]) / 2, x[-1] + (x[0] - x[1]) / 2])
    plt.xlabel('$\Gamma_0$', size=25)
    plt.xticks(fontsize=20)

    plt.ylabel('$\langle f_{ZZ} \\rangle$',size=25)
    plt.yticks(fontsize=20)

    plt.plot(x_grid, y_grid, linewidth=3, linestyle='--', c='r')
    plt.errorbar(x, y, yerr=y_err, marker='o', ls='', capsize=5, capthick=1, ecolor='black', color='k')

    plt.tight_layout()

    plt.savefig(carpeta + '/freq_processed/plot', dpi=300)
    plt.show()
    plt.close()