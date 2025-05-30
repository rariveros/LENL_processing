from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'F'
    initial_dir_data = str(disco) + ':/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')
    folder_list = os.listdir(directory)

    ###    Iterando carpetas    ###
    for j in folder_list:
        n = folder_list.index(j) + 1
        X_mm = np.loadtxt(directory + '/' + j + '/X_mm.txt', delimiter=',')
        T_s = np.loadtxt(directory + '/' + j + '/T_s.txt', delimiter=',')
        Z_mm = np.loadtxt(directory + '/' + j + '/Z_mm.txt', delimiter=',')
        Nx = len(X_mm)
        Nt = len(T_s)

        ###    Obteniendo información de medidas experimentales    ###
        zero_fix = 'no'  # Activar para solitones, no para patrones
        file_name = os.path.basename(directory + '/' + j)
        print('Procesando archivo ' + file_name + ' (' + str(n) + '/' + str(len(folder_list)) + ')')
        name_list = file_name.split("_")
        a = float(name_list[0].split("=")[-1])
        forcing_freq = float(name_list[1].split("=")[-1])
        GAMMA_0 = int(((((forcing_freq / 2) / (2 * np.pi)) ** 2) * (a / 12) * 0.5) * 100) * 0.01
        fps = 150
        period_fps = int(fps * (2 / forcing_freq))
        period_error_range = 8

        ###    Inicialización de ventana inicial de búsqueda de máximos    ###
        T_big_initial = 100
        big_initial_window = Z_mm[0:T_big_initial, :]
        i_max, j_max = np.unravel_index(big_initial_window.argmax(), big_initial_window.shape)

        ###    Definiendo tamaño de ventana espacial e iterando en el espaciotemporal    ###
        initial_window_size = 20  # Numero PAR
        Z_strobo = []
        T_strobo = []
        while i_max < Nt - period_fps - period_error_range / 2:
            window = Z_mm[int(i_max - period_error_range / 2):int(i_max + period_error_range / 2),
                     int(j_max - initial_window_size / 2):int(j_max + initial_window_size / 2)]
            i_max_new, j_max_new = np.unravel_index(window.argmax(), window.shape)
            i_max_Z = i_max + period_fps - period_error_range / 2 + i_max_new
            j_max_Z = j_max - initial_window_size / 2 + j_max_new
            Z_strobo.append(Z_mm[int(i_max_Z), :])
            T_strobo.append(T_s[int(i_max_Z)])
            Z_strobo_np = np.array(Z_strobo)
            T_strobo_np = np.array(T_strobo)
            i_max = i_max_Z
            j_max = j_max_Z

        ###    Filtros para visualización    ###
        Z_strobo_np = filtro_superficie(Z_strobo_np, 2, 'Y')

        ###    Guardado de datos y corrección de cero para solitones    ###
        if zero_fix == 'yes':
            Z_strobo_np[Z_strobo_np < 0] = 0
        np.savetxt(directory + '/' + j + '/T_stroboscopic.txt', T_strobo_np, delimiter=',')
        np.savetxt(directory + '/' + j + '/Z_mm_stroboscopic.txt', Z_strobo_np, delimiter=',')

        ###    Generando y guardando espaciotemporal de vista estroboscopica     ###
        norm = TwoSlopeNorm(vmin=np.amin(Z_strobo_np), vcenter=0, vmax=np.amax(Z_strobo_np))
        pcm = plt.pcolormesh(X_mm, np.arange(len(Z_strobo_np[:, 0])), Z_strobo_np, norm=norm, cmap='seismic',
                             shading='auto')
        cbar = plt.colorbar(pcm, shrink=1)
        cbar.set_label('$|\psi(x, t)|$', rotation=0, size=20, labelpad=-27, y=1.1)
        plt.title('$\Gamma_0 = $' + str(GAMMA_0).split(".")[0] + '.' + str(GAMMA_0).split(".")[1][0:2] + '   $f_{forc} = $' + str(forcing_freq) + ' hz', size='15')
        plt.xlim([X_mm[0], X_mm[-1]])
        plt.xlabel('$x$', size='20')
        plt.ylabel('$t$', size='20')
        plt.grid(linestyle='--', alpha=0.5)
        plt.savefig(directory + '/' + j + '/stroboscopic.png', dpi=300)
        plt.close()
