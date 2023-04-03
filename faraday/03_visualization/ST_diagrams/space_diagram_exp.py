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

    a = 6.5
    f = 14.6
    gamma_0 = f ** 2 * a * 8.401093 * 10 ** (-5)

    # FIXES
    #X = X[8:-9]
    fig, ax = plt.subplots()
    ti, tf = 0, -1

    # legend
    pcm = plt.pcolormesh(X, T[ti:tf], Z[ti:tf, :] - 4, cmap=parula_map, vmin=np.amin(Z), vmax=np.amax(Z), shading='auto')
    cbar = plt.colorbar(pcm)
    cbar.set_label('$A_R(x, t)$', rotation=0, size=25, labelpad=-27, y=1.11)
    plt.title('$\Gamma_0 =%.3f' % (gamma_0,) + '$   $f_i = ' + str(f) + '\ \\textrm{hz}$ ', size='15')

    # put the major ticks at the middle of each cell
    plt.xlim([X[0], X[-1]])
    plt.xlabel('$x\ (\\textrm{mm})$', size='25')
    plt.xticks([-300, -200, -100, 0, 100, 200, 300], fontsize=20)

    #plt.ylim([20, 80])
    plt.ylabel('$t\ (\\textrm{s})$', size='25')
    plt.yticks(fontsize=20)
    #plt.ylim([0, 0.5])

    plt.grid(linestyle='--', alpha=0.2, color='k')
    cbar.ax.tick_params(labelsize=15)

    # labels
    plt.tight_layout()
    plt.savefig(directory + '/strobo_maximum.png', dpi=300)
    plt.close()