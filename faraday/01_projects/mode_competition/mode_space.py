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
    freq_k = (n / X_period)
    print(freq_k)

    Z_mode_intensity = np.abs(Z_FFT)
    for i in range(len(T)):
        Z_mode_intensity = Z_mode_intensity / np.sum(Z_mode_intensity[i, :])
    ref = np.amax(Z_mode_intensity)
    # legend
    pcm = plt.pcolormesh(freq_k[:Nx // 2], T, np.log(Z_mode_intensity[:, :Nx // 2]) - np.log(ref), cmap=parula_map, vmin=-3, vmax=1, shading='auto')
    pcm = plt.pcolormesh(freq_k[:Nx // 2], T, Z_mode_intensity[:, :Nx // 2] , cmap=parula_map, vmin=np.amin(Z_mode_intensity), vmax=np.amax(Z_mode_intensity), shading='auto')
    #pcm = plt.pcolormesh(freq_k, T, Z_mode_intensity, cmap=parula_map,
    #                     vmin=np.amin(Z_mode_intensity), vmax=np.amax(Z_mode_intensity), shading='auto')
    cbar = plt.colorbar(pcm)
    cbar.set_label('$\hat{A}_R(k_x, t)$', rotation=0, size=25, labelpad=-27, y=1.13)

    # put the major ticks at the middle of each cell
    plt.xlim([0, 0.05])
    plt.xlabel('$k\ (\\textrm{mm}^{-1})$', size='25')
    plt.xticks(fontsize=20)

    #plt.ylim([0, 10])
    plt.ylabel('$t\ (\\textrm{s})$', size='25')
    plt.yticks(fontsize=20)

    plt.grid(linestyle='--', alpha=0.2, color='k')
    cbar.ax.tick_params(labelsize=15)

    # labels
    plt.tight_layout()
    plt.savefig('mode_interaction_example.png', dpi=300)
    plt.close()