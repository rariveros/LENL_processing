from directories import *
from back_process import *


if __name__ == "__main__":
    disco = 'N:'
    initial_dir_data = str(disco) + ':/mnustes_science/simulation_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')
    X = np.loadtxt(directory + '/X.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_s.txt', delimiter=',')

    period = 1 / 400
    Nt = len(T)
    Nx = len(X)

    Z_FFT = []
    for i in range(Nx):
        yf = fft(Z[:, i])
        Z_FFT.append(yf)
    FFT_mean = np.mean(Z_FFT, axis=0)
    xf = fftfreq(Nt, period)[:Nt // 2]
    #plt.plot(xf[1:-1],
    #         (2.0 / Nt * np.abs(FFT_mean[0:Nt // 2]))[
    #         1:-1])
    plt.plot(xf[1:-1], (np.log(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2])) - np.log(np.amax(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2]))))[1:-1], c='k', zorder=10)
    plt.fill_between(xf[1:-1],
                     np.amin((np.log(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2])) - np.log(np.amax(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2]))))[1:-1]),
                     (np.log(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2])) - np.log(np.amax(2.0 / Nt * np.abs(FFT_mean[0:Nt // 2]))))[1:-1], color='k', zorder=10)
    plt.xlim([0, 1.4])
    y_min = -8
    y_max = 2
    plt.ylim([y_min, y_max])
    plt.vlines(14.8, y_min, y_max, colors=['r'], linestyles=['dotted'])
    plt.vlines(7.4, y_min, y_max, colors=['r'], linestyles=['dotted'])
    plt.vlines(0.26, y_min, y_max, colors=['r'], linestyles=['dotted'])
    plt.grid(linestyle='--', alpha=0.2, color='k')

    plt.ylabel('$\ln(I/I_0)$ \\textrm{(dB)}', size=25)
    plt.xticks(fontsize=20)

    plt.xlabel('$f_i$', size=25)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig(directory + '/spectrum_analysis_zoom.png', dpi=300)
    plt.close()

