from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'E'
    initial_dir_data = str(disco) + ':/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X_mm = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    X_mm = X_mm #* (30 / 40)
    T_s = np.loadtxt(directory + '/T_s.txt', delimiter=',')
    Z_mm = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')

    ###    Obteniendo información de medidas experimentales    ###
    zero_fix = 'no'  # Activar para solitones, no para patrones

    Nx = len(X_mm)
    Nt = len(T_s)

    file_name = os.path.basename(directory)
    name_list = file_name.split("_")
    notation = 'fa'
    if notation == 'fa':
        f_i = float(name_list[0].split("=")[-1])
        a = float(name_list[1].split("=")[-1])
    elif notation == 'af':
        a = float(name_list[0].split("=")[-1])
        f_i = float(name_list[1].split("=")[-1])
    n_pistones = 6
    fps = 400

    period_fps = int(fps * (2 / f_i))
    T_window_length = 3 * period_fps
    N = len(T_s) // T_window_length

    Z_strobo = []
    T_strobo = []
    for i in range(N - 1):
        Z_bin = Z_mm[T_window_length * i:T_window_length * (i + 1), :]
        Z_strobo_i = np.sqrt(2) * np.std(Z_bin, axis=0)
        Z_strobo.append(Z_strobo_i)
        T_strobo.append(T_s[T_window_length * i])
    Z_strobo_np = np.array(Z_strobo)
    T_strobo_np = np.array(T_strobo)

    alpha, beta, nu, gamma = fluid_pdnls_parameters(f_i, a, d=20)
    sigma = 18.46 * n_pistones #aaaaaaaaaaaaa

    alpha_str = str(alpha).split(".")[0] + '.' + str(alpha).split(".")[1][0:3]
    beta_str = str(beta).split(".")[0] + '.' + str(beta).split(".")[1][0:5]
    nu_str = str(nu).split(".")[0] + '.' + str(nu).split(".")[1][0:3]
    gamma_str = str(gamma).split(".")[0] + '.' + str(gamma).split(".")[1][0:3]
    sigma_str = str(sigma).split(".")[0] + '.' + str(sigma).split(".")[1][0:1]

    np.savetxt(directory + '/T_stroboscopic.txt', T_strobo_np, delimiter=',')
    np.savetxt(directory + '/Z_mm_stroboscopic.txt', Z_strobo_np, delimiter=',')


    ###    Generando y guardando espaciotemporal de vista estroboscopica     ###
    pcm = plt.pcolormesh(X_mm, T_strobo, Z_strobo_np, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$|A_R(x, t)|$', rotation=0, size=13, labelpad=-27, y=1.1)
    plt.title('$\gamma_0 = ' + gamma_str + '\ f_i = ' + str(f_i) + '\ \\textrm{Hz}' +
              '\ \\alpha = ' + alpha_str  + '\ \\textrm{mm}^{2}' + '\ \\beta = ' + beta_str + '\ \\nu = ' + nu_str + '$', size='10')
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/stroboscopic.png', dpi=300)
    plt.show()
    plt.close()


