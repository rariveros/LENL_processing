from directories import *
from back_process import *


if __name__ == "__main__":

    ### Definiendo parametros y eligiendo carpeta a detectar ###
    disco = 'E:'
    project_file = 'PT_01'
    initial_dir_img = str(disco) + '/mnustes_science/images'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askdirectory(parent=root, initialdir=initial_dir_img, title='Elección de carpeta')
    parent_file_name = os.path.basename(file)
    save_directory = 'E:/mnustes_science/experimental_data/' + project_file + '/' + parent_file_name
    IMG_names = os.listdir(file)
    N_img = len(IMG_names)
    resize_scale = 1
    thresh = 48


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
    threshold_01 = 140
    threshold_02 = 110
    radius = 20


    ### Binarize images with 0 and 1 ###
    img_binarized = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    img_binary = img_binarized / 255

    ### Se genera un operador similar a Dx sparse y un vector contador ###
    D = sparse_D(Ny)
    enumerate_array = np.arange(Ny)[::-1]
    ones_array = np.ones(Ny)
    # Midiendo tiempo inicial
    now = datetime.datetime.now()
    print('Hora de Inicio: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_init = time.time()
    ### Iteración de detección ###
    Z = []
    for i in range(N_img):
        img_i = cv2.imread(file + '/' + IMG_names[i])
        img_crop = img_i[y_1:(y_1 + y_2), x_1:(x_1 + x_2)]
        img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_canned = cv2.Canny(img_blur, threshold_01, threshold_02)
        #plt.plot(img_canned[:, i])
        #plt.imshow(img_canned)
        #plt.show()
        Z_i = []
        #print('i=' + str(i))
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
    #for i in range(len(Z[:, 0]) - 1):
    #    for j in range(len(Z[0, :]) - 2):
    #        if Z[i, 1 + j] - Z[i, 1 + j + 1] > radius:
    #            Z[i, 1 + j + 1] = Z[i, 1 + j]

    one_vect = np.ones(N_img)
    Z_leveled = np.zeros((N_img, Nx))
    for i in range(Nx):
        Z_leveled[:, i] = Z[:, i] - np.mean(Z[:, i]) * one_vect

    # Midiendo tiempo final
    now = datetime.datetime.now()
    print('Hora de Término: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_fin = time.time()
    print(str(time_fin - time_init) + ' seg')

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
    #plt.plot([IL_L, IL_R], [T_s[-1] / 10, T_s[-1] / 10], color='r')
    #plt.plot([IL_L, IL_L], [T_s[-1] / 10 - T_s[-1] / 25, T_s[-1] / 10 + T_s[-1] / 25], color='r')
    #plt.plot([IL_R, IL_R], [T_s[-1] / 10 - T_s[-1] / 25, T_s[-1] / 10 + T_s[-1] / 25], color='r')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(save_directory + '/water_level.png', dpi=1000)
    plt.close()
