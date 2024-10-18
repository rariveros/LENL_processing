from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'E'
    initial_dir_data = str(disco) + ':/Users/mnustes_science/PT_fluids/mnustes_science'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir="r" + initial_dir_data, title='Elección de carpeta')

    X_mm = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T_s = np.loadtxt(directory + '/T_s.txt', delimiter=',')
    Z_mm = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')

    ###    Obteniendo información de medidas experimentales    ###
    zero_fix = 'no'  # Activar para solitones, no para patrones

    Nx = len(X_mm)
    Nt = len(T_s)

    file_name = os.path.basename(directory)
    name_list = file_name.split("_")
    notation = 'af'
    if notation == 'fa':
        forcing_freq = float(name_list[0].split("=")[-1])
        a = float(name_list[1].split("=")[-1])
    elif notation == 'af':
        a = float(name_list[0].split("=")[-1])
        forcing_freq = float(name_list[1].split("=")[-1])
    GAMMA_0 = int(((((forcing_freq / 2) / (2 * np.pi)) ** 2) * (a / 12) * 0.5) * 100) * 0.01

    fps = 400
    period_fps = int(fps * (2 / forcing_freq))
    print(period_fps)
    period_error_range = 12

    ###    Inicialización de ventana inicial de búsqueda de máximos    ###
    T_big_initial = 200
    big_initial_window = Z_mm[100:T_big_initial, :]
    i_max, j_max = np.unravel_index(big_initial_window.argmax(), big_initial_window.shape)

    ###    Definiendo tamaño de ventana espacial e iterando en el espaciotemporal    ###
    initial_window_size = 30   # Numero PAR
    Z_strobo = []
    T_strobo = []
    I_strobo = []
    n = 0
    while i_max < Nt - 5 * period_fps:
        window = Z_mm[int(i_max - period_error_range / 2):int(i_max + period_error_range / 2), int(j_max - initial_window_size / 2):int(j_max + initial_window_size / 2)]
        i_max_new, j_max_new = np.unravel_index(window.argmax(), window.shape)
        i_max_Z = i_max + period_fps - period_error_range / 2 + i_max_new
        j_max_Z = j_max - initial_window_size / 2 + j_max_new
        if n % 10 == 0:
            big_window = Z_mm[int(i_max_Z), :]
            j_max_Z = np.unravel_index(big_window.argmax(), big_window.shape)[0]
            print(j_max_Z)
        Z_strobo.append(Z_mm[int(i_max_Z), :])
        T_strobo.append(T_s[int(i_max_Z)])
        I_strobo.append(int(i_max_Z))
        i_max = i_max_Z
        j_max = j_max_Z
        n = n + 1
        print(n)
    Z_strobo_np = np.array(Z_strobo)
    T_strobo_np = np.array(T_strobo)
    I_strobo_np = np.array(I_strobo)

    ###    Filtros para visualización    ###
    Z_strobo_np = filtro_superficie(Z_strobo_np, 10, 'X')
    Z_strobo_np = filtro_superficie(Z_strobo_np, 4, 'Y')

    ###    Guardado de datos y corrección de cero para solitones    ###
    if zero_fix == 'yes':
        Z_strobo_np[Z_strobo_np < 0] = 0
    np.savetxt(directory + '/T_stroboscopic.txt', T_strobo_np, delimiter=',')
    np.savetxt(directory + '/Z_mm_stroboscopic.txt', Z_strobo_np, delimiter=',')
    np.savetxt(directory + '/I_stroboscopic.txt', I_strobo_np, delimiter=',')

    ###    Generando y guardando espaciotemporal de vista estroboscopica     ###
    norm = TwoSlopeNorm(vmin=-np.amax(Z_strobo_np), vcenter=0, vmax=np.amax(Z_strobo_np)) # pattern o multi-soliton
    #norm = TwoSlopeNorm(vmin=np.amin(Z_strobo_np), vcenter=np.amax(Z_strobo_np) / 2, vmax=np.amax(Z_strobo_np))  # 1-soliton
    pcm = plt.pcolormesh(X_mm, T_strobo_np, Z_strobo_np, norm = norm, cmap=parula_map, shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$A_{R}(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.title('$\Gamma_0 = ' + str(GAMMA_0) + '$   $f_i = ' + str(forcing_freq) + '\ hz$ ', size='15')
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/stroboscopic.png', dpi=300)
    plt.close()
