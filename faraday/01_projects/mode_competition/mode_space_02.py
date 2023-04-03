from directories import *
from back_process import *


if __name__ == "__main__":
    disco = 'N:'
    initial_dir_data = str(disco) + ':/mnustes_science/simulation_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_mm_stroboscopic.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_stroboscopic.txt', delimiter=',')

    Nx = len(X)
    Nt = len(T)

    Z_FFT = []
    for i in range(Nt):
        yf = fft(Z[i, :])
        Z_FFT.append(yf)
    Z_FFT = np.array(Z_FFT)
    N = len(Z_FFT[0, :])
    n = np.arange(N)
    sr = 1 / np.abs(X[1] - X[0])
    X_period = N / sr
    freq_k = (2 * np.pi * (n / X_period) * (240 / np.pi))[:Nx // 2]
    print(freq_k[:15])

    Z_mode_intensity = np.abs(Z_FFT[:, :Nx // 2])
    ref = np.amax(Z_mode_intensity)
    plt.plot(T, np.log(Z_mode_intensity[:, 5]) - np.log(ref), c='r', label='$n=5$')
    plt.plot(T, np.log(Z_mode_intensity[:, 6]) - np.log(ref), c='k', label='$n=6$')
    plt.plot(T, np.log(Z_mode_intensity[:, 13]) - np.log(ref), c='b', label='$n=14$')

    plt.legend(loc='lower right', fontsize=15)
    plt.grid('--', alpha=0.2)
    plt.xlim([T[0], T[-1]])
    plt.ylim([-2, 0.05])
    plt.xlabel('$t\ \\textrm{(s)}$', size=30)
    plt.ylabel('$\ln(I/I_0)$ \\textrm{(dB)}', size=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig('mode_interaction_.png', dpi=300)
    plt.show()