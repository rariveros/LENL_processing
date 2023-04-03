from directories import *
from back_process import *


if __name__ == "__main__":
    disco = 'C'
    initial_dir_data = "E:\PC\mnustes_science\PT_fluids\mnustes_science\simulation_data\FD\PNDLS\gaussian\mu=0.1\gamma=0.450\\nu=0.35\sigma=10.0"
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z_real = np.loadtxt(directory + '/field_real.txt', delimiter=',')
    Z_img = np.loadtxt(directory + '/field_img.txt', delimiter=',')
    T = np.loadtxt(directory + '/T.txt', delimiter=',')
    X = np.loadtxt(directory + '/X.txt', delimiter=',')
    Nt = len(T)
    Nx = len(X)
    dt = T[1] - T[0]
    dx = X[1] - X[0]

    Z_complex_1 = Z_real + 1j * Z_img

    Z_real_1 = filtro_superficie(Z_real, 40, "Y")
    Z_img_1 = filtro_superficie(Z_img, 40, "Y")
    Z_complex_2 = Z_real_1 + 1j * Z_img_1

    arg_1 = np.angle(Z_complex_1)
    arg_2 = np.angle(Z_complex_2)

    D = sparse_D(Nt, dt)
    DZ_real = Dx(D, Z_real_1)

    pcm_1 = plt.pcolormesh(X, T, Z_real_1, cmap=parula_map, shading='auto')
    cbar_1 = plt.colorbar(pcm_1, shrink=1)
    cbar_1.set_label('$\\textrm{arg}(A)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X[0], X[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.title("$\\textrm{Filtered}$", size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/real_filtered.png', dpi=300)
    plt.close()

    #norm_2 = TwoSlopeNorm(vmin=-0.5, vcenter=0, vmax=0.5)
    pcm_2 = plt.pcolormesh(X, T, DZ_real, cmap=parula_map, shading='auto')
    cbar_2 = plt.colorbar(pcm_2, shrink=1)
    cbar_2.set_label('$\\textrm{arg}(A)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X[0], X[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.title("$\\textrm{No Filter}$", size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/der_Z_real.png', dpi=300)
    plt.close()