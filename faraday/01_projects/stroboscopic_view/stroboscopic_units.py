from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'F'
    initial_dir_data = str(disco) + ':/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X = np.loadtxt(directory + '/X.txt')
    T = np.loadtxt(directory + '/T.txt')
    Z = np.loadtxt(directory + '/Z.txt')

    ### Abriendo imagen de referencia para determinar la región de interes (ROI) y la conversion a mm ###
    resize_scale = 1

    root = tk.Tk()
    root.withdraw()
    reference_image = filedialog.askopenfilename(parent=root, initialdir=str(disco) + ':/mnustes_science', title='Reference Selection')
    img_reference = cv2.imread(str(reference_image))


    ### Resize image for ROI selection ###
    h, w, c = img_reference.shape
    h_resized, w_resized = h * resize_scale,  w * resize_scale
    resized_img = cv2.resize(img_reference, (int(w_resized), int(h_resized)))

    FC_mm = pix_to_mm(resized_img, resize_scale)
    IL_L, IL_R = injection_length(resized_img, resize_scale)

    fps = 400
    Nx = len(X)
    X_mm = FC_mm * X - (FC_mm * X[-1] / 2) * np.ones(Nx)
    IL_L = FC_mm * IL_L - (FC_mm * X[-1] / 2)
    IL_R = FC_mm * IL_R - (FC_mm * X[-1] / 2)
    IL_mm = np.array([IL_L, IL_R])
    T_s = T / fps
    Z_mm = FC_mm * Z

    np.savetxt(directory + '/X_mm.txt', X_mm, delimiter=',')
    np.savetxt(directory + '/T_s.txt', T_s, delimiter=',')
    np.savetxt(directory + '/Z_mm.txt', Z_mm, delimiter=',')

    ###    Obteniendo información de medidas experimentales    ###
    zero_fix = 'no'  # Activar para solitones, no para patrones

    Nx = len(X_mm)
    Nt = len(T_s)

    file_name = os.path.basename(directory)
    name_list = file_name.split("_")
    a = float(name_list[0].split("=")[-1])

    forcing_freq = float(name_list[1].split("=")[-1])
    GAMMA_0 = int(((((forcing_freq / 2) / (2 * np.pi)) ** 2) * (a / 12) * 0.5) * 100) * 0.01

    fps = 400
    period_fps = int(fps * (2 / forcing_freq))
    print(period_fps)
    period_error_range = 8

    ###    Inicialización de ventana inicial de búsqueda de máximos    ###
    T_big_initial = 100
    big_initial_window = Z_mm[0:T_big_initial, :]
    i_max, j_max = np.unravel_index(big_initial_window.argmax(), big_initial_window.shape)

    ###    Definiendo tamaño de ventana espacial e iterando en el espaciotemporal    ###
    initial_window_size = 20   # Numero PAR
    Z_strobo = []
    T_strobo = []
    while i_max < Nt - period_fps:
        window = Z_mm[int(i_max - period_error_range / 2):int(i_max + period_error_range / 2), int(j_max - initial_window_size / 2):int(j_max + initial_window_size / 2)]
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
    Z_strobo_np = filtro_superficie(Z_strobo_np, 4, 'Y')

    ###    Guardado de datos y corrección de cero para solitones    ###
    if zero_fix == 'yes':
        Z_strobo_np[Z_strobo_np < 0] = 0
    np.savetxt(directory + '/T_stroboscopic.txt', T_strobo_np, delimiter=',')
    np.savetxt(directory + '/Z_mm_stroboscopic.txt', Z_strobo_np, delimiter=',')

    ###    Generando y guardando espaciotemporal de vista estroboscopica     ###
    norm = TwoSlopeNorm(vmin=np.amin(Z_strobo_np), vcenter=0, vmax=np.amax(Z_strobo_np)) # pattern o multi-soliton
    #norm = TwoSlopeNorm(vmin=np.amin(Z_strobo_np), vcenter=np.amax(Z_strobo_np) / 2, vmax=np.amax(Z_strobo_np))  # 1-soliton
    pcm = plt.pcolormesh(X_mm, np.arange(len(Z_strobo_np[:, 0])), Z_strobo_np, norm = norm, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$Re(\psi)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.title('$\Gamma_0 = $' + str(GAMMA_0) + '   $f_{forc} = $' + str(forcing_freq) + ' hz', size='15')
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/stroboscopic.png', dpi=300)
    plt.close()
