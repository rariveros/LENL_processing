from directories import *
from back_process import *


if __name__ == "__main__":
    disco = 'N:'
    initial_dir_data = str(disco) + ':/mnustes_science/simulation_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_strobo.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_strobo.txt', delimiter=',')
    Z = filtro_superficie(Z, 3, "YX")
    Nx = len(X)
    # FIXES
    fig, ax = plt.subplots()
    ti, tf = 10, 49
    xi, xf = -200, 200

    # plt.plot(X, arg[ti, :])
    # plt.show()

    # legend
    pcm = plt.pcolormesh(X[int(0.00 * Nx):]-8, (T - ti) * 16, Z[:, int(0.00 * Nx):], cmap=parula_map, shading='auto')
    cbar = plt.colorbar(pcm)
    cbar.set_label('$|A_R(x,t)|$', rotation=0, size=25, labelpad=-27, y=1.11)

    # put the major ticks at the middle of each cell
    plt.xlim([xi, xf])
    plt.xlabel('$x$', size='25')
    plt.xticks(fontsize=15)

    plt.ylim([0, (tf - ti) * 16])
    plt.ylabel('$t/T$', size='25')
    plt.yticks(fontsize=15)

    plt.grid(linestyle='--', alpha=0.2, color='k')
    cbar.ax.tick_params(labelsize=15)

    # labels
    plt.tight_layout()
    plt.savefig(directory + '/field_visual.png', dpi=300)
    plt.close()