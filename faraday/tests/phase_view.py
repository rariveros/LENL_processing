from directories import *
from back_process import *
from scipy.signal import correlate

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
    nsamples = 120
    A = Z_mm[0:nsamples, i_max]
    A -= A.mean();
    A /= A.std()
    Z_phase = []
    dt = np.arange(1 - nsamples, nsamples)
    I_phase = np.arange(0, Nt, nsamples)
    T_phase =[]
    for i in I_phase:
        Z_phase_i = []
        for j in range(Nx):
            B = Z_mm[i: i + nsamples, j]
            B -= B.mean();
            B /= B.std()
            xcorr = correlate(A, B)
            Z_phase_i.append(dt[xcorr.argmax()])
        T_phase.append(T_s[i])
        Z_phase_i = np.array(Z_phase_i)
        Z_phase.append(Z_phase_i)
    T_phase = np.array(T_phase)
    Z_phase = np.array(Z_phase)

    ###    Generando y guardando espaciotemporal de vista estroboscopica     ###
    pcm = plt.pcolormesh(X_mm, T_phase, Z_phase, cmap=parula_map, shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\phi(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/Z_phase.png', dpi=300)
    plt.close()
