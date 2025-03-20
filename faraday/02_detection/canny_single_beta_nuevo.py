from back_process import *


if __name__ == "__main__":

    ### Definiendo parametros y eligiendo carpeta a detectar ###
    disco = 'D:'
    project_file = 'soliton_control'
    initial_dir_img = str(disco) + '/mnustes_science/images/img_lab/soliton_control/espacio_parametros'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data/soliton_control/espacio_parametros/'
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askdirectory(parent=root, initialdir=initial_dir_img, title='Elección de carpeta')
    parent_file_name = os.path.basename(file)
    save_directory = disco + '/mnustes_science/experimental_data/soliton_control/espacio_parametros/' + '/' + parent_file_name
    IMG_names = os.listdir(file)
    N_img = len(IMG_names)
    resize_scale = 0.85

    def nan_helper(y):
        return np.isnan(y), lambda z: z.nonzero()[0]

    ### Abriendo imagen de referencia para determinar la región de interes (ROI) y la conversion a mm ###
    root = tk.Tk()
    root.withdraw()
    reference_image = filedialog.askopenfilename(parent=root, initialdir=file, title='Reference Selection')
    img_reference = cv2.imread(str(reference_image))


    ### Resize image for ROI selection ###
    h, w, c = img_reference.shape
    h_resized, w_resized = h * resize_scale,  w * resize_scale
    resized_img = cv2.resize(img_reference, (int(w_resized), int(h_resized)))
    cut_coords = cv2.selectROI(resized_img)
    cv2.destroyAllWindows()


    FC_mm = pix_to_mm(resized_img, resize_scale)
    IL_L, IL_R = injection_length(resized_img, resize_scale)

    ### Cut image with resized scale ###
    cut_coords_list = list(cut_coords)
    x_1 = int(cut_coords_list[0] / resize_scale)
    x_2 = int(cut_coords_list[2] / resize_scale)
    y_1 = int(cut_coords_list[1] / resize_scale)
    y_2 = int(cut_coords_list[3] / resize_scale)
    img_crop = img_reference[y_1:(y_1 + y_2), x_1:(x_1 + x_2)]
    img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    Ny, Nx = img_gray.shape
    threshold_01 = 240
    threshold_02 = 200
    radius = 20
    gamma = 1.0 #1.0
    alpha = 1.0 #1.0
    beta = 0.0 #0.0

    ### Se genera un operador similar a Dx sparse y un vector contador ###
    enumerate_array = np.arange(Ny)[::-1]
    ones_array = np.ones(Ny)

    # Midiendo tiempo inicial
    now = datetime.datetime.now()
    print('Hora de Inicio: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_init = time.time()

    ### Iteración de detección ###
    Z = []
    plot = "no"
    for i in range(N_img):
        img_i = cv2.imread(file + '/' + IMG_names[i])
        img_crop = img_i[y_1:(y_1 + y_2), x_1:(x_1 + x_2)]
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
        #img_processed = image_corrections(img_crop, alpha, beta, gamma)
        img_processed = img_crop
        img_blur = cv2.GaussianBlur(img_processed, (7, 7), 0)

        # ADAPTATIVE BINARIZATION / SIMPLE BINARIZATION
        hist = cv2.calcHist([img_blur], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()
        Q = hist_norm.cumsum()
        bins = np.arange(256)
        fn_min = np.inf
        thresh = -1
        for j in range(1, 256):
            p1, p2 = np.hsplit(hist_norm, [j])  # probabilities
            q1, q2 = Q[j], Q[255] - Q[j]  # cum sum of classes
            if q1 < 1.e-6 or q2 < 1.e-6:
                continue
            b1, b2 = np.hsplit(bins, [j])  # weights
            # finding means and variances
            m1, m2 = np.sum(p1 * b1) / q1, np.sum(p2 * b2) / q2
            v1, v2 = np.sum(((b1 - m1) ** 2) * p1) / q1, np.sum(((b2 - m2) ** 2) * p2) / q2
            # calculates the minimization function
            fn = v1 * q1 + v2 * q2
            if fn < fn_min:
                fn_min = fn
            thresh = j
        ret, img_processed = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #img_processed = cv2.adaptiveThreshold(img_processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        #cret, img_processed = cv2.threshold(img_processed, 50, 255, cv2.THRESH_BINARY)
        img_canned = cv2.Canny(img_processed, threshold_01, threshold_02)
        if plot == "si" and i % 10 == 0:
            #AGREGAR GIF PARA 3 PERIODOS DE CONFIRMACIÓN DE DETECCION
            fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
            ax1.imshow(img_crop, cmap='gray', vmin=0, vmax=255)
            ax2.imshow(img_processed, cmap='gray', vmin=0, vmax=255)
            ax3.imshow(img_canned, cmap='viridis', vmin=0, vmax=255)
            plt.show()
            plt.close()
        Z_i = []
        for j in range(Nx):
            normalization = np.dot(ones_array, img_canned[:, j])
            if normalization != 255:
                position = np.nan
            else:
                position = np.dot(enumerate_array, img_canned[:, j]) / normalization
            Z_i.append(position)
        Z_i = np.array(Z_i)
        nans, x = nan_helper(Z_i)
        Z_i[nans] = np.interp(x(nans), x(~nans), Z_i[~nans])
        Z.append(Z_i)
    Z = np.array(Z)

    one_vect = np.ones(N_img)
    Z_leveled = np.zeros((N_img, Nx))
    for i in range(Nx):
        Z_leveled[:, i] = Z[:, i] - np.mean(Z[:, i]) * one_vect

    # Midiendo tiempo final
    now = datetime.datetime.now()
    print('Hora de Término: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_fin = time.time()
    print(str(time_fin - time_init) + ' seg')
    print(parent_file_name)

    ### Definiendo espacio-temporal en numpy en pixeles y mm ##
    fps = 400
    X = np.arange(Nx)
    X_mm = FC_mm * X - (FC_mm * X[-1] / 2) * np.ones(Nx)
    IL_L = FC_mm * IL_L - (FC_mm * X[-1] / 2)
    IL_R = FC_mm * IL_R - (FC_mm * X[-1] / 2)
    IL_mm = np.array([IL_L, IL_R])
    T = np.arange(N_img)
    T_s = T / fps
    print(X_mm[-1])
    Z_mm = FC_mm * Z_leveled

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    np.savetxt(save_directory + '/X.txt', X, delimiter=',')
    np.savetxt(save_directory + '/X_mm.txt', X_mm, delimiter=',')
    np.savetxt(save_directory + '/T.txt', T, delimiter=',')
    np.savetxt(save_directory + '/T_s.txt', T_s, delimiter=',')
    np.savetxt(save_directory + '/Z.txt', Z, delimiter=',')
    np.savetxt(save_directory + '/Z_mm.txt', Z_mm, delimiter=',')
    np.savetxt(save_directory + '/IL_mm.txt', IL_mm, delimiter=',')


    ### Visualizacion del diagrama espacio-temporal  ###
    norm = TwoSlopeNorm(vmin=np.amin(Z_mm), vcenter=0, vmax=np.amax(Z_mm))
    pcm = plt.pcolormesh(X_mm, T_s, Z_mm, norm=norm, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(save_directory + '/water_level.png', dpi=1000)
    plt.close()
