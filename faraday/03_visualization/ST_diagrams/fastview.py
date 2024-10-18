from directories import *
from back_process import *


if __name__ == "__main__":
    disco = 'N:'
    initial_dir_data = str(disco) + ':/mnustes_science/simulation_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_s.txt', delimiter=',')

    file_name = os.path.basename(directory)
    name_list = file_name.split("_")
    notation = 'fa'
    if notation == 'fa':
        f_i = float(name_list[0].split("=")[-1])
        a = float(name_list[1].split("=")[-1])
    elif notation == 'af':
        a = float(name_list[0].split("=")[-1])
        f_i = float(name_list[1].split("=")[-1])
    alpha, beta, nu, gamma = fluid_pdnls_parameters(f_i, a, d=20)

    # FIXES
    #X = X[8:-9]
    fig, ax = plt.subplots()
    ti, tf = 0, -1
    x0 = 0

    # legend
    #norm = colors.TwoSlopeNorm(vmin=0, vmax=np.amax(Z))
    pcm = plt.pcolormesh(X - x0, T[ti:tf], Z[ti:tf, :], cmap=parula_map, shading='auto')
    cbar = plt.colorbar(pcm)
    cbar.set_label('$|A(x, t)|$', rotation=0, size=25, labelpad=-27, y=1.11)
    #plt.title('$\gamma_0 =%.3f' % (gamma,) + '$   $f_i = ' + str(f_i) + '\ \\textrm{Hz}$ ', size='15')

    # put the major ticks at the middle of each cell
    plt.xlim([-100, 100])
    plt.xlabel('$x\ (\\textrm{mm})$', size='25')
    plt.xticks(fontsize=18)

    #plt.ylim([20, 80])
    plt.ylabel('$t\ (\\textrm{s})$', size='25')
    plt.yticks(fontsize=18)
    plt.ylim([0, 1])

    plt.grid(linestyle='--', alpha=0.2, color='k')
    cbar.ax.tick_params(labelsize=15)

    # labels
    plt.tight_layout()
    plt.savefig(directory + '/fastview.png', dpi=300)
    plt.close()