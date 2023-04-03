from directories import *
from back_process import *


if __name__ == "__main__":

    ### Definiendo parametros y eligiendo carpeta a detectar ###
    disco = 'C:'
    project_file = 'front_propagation'
    initial_dir_img = str(disco) + '/mnustes_science/images'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data'

    root = tk.Tk()
    root.withdraw()
    file = filedialog.askdirectory(parent=root, initialdir=initial_dir_img, title='Elección de carpeta')
    parent_file_name = os.path.basename(file)
    save_directory = initial_dir_data + '/' + project_file + '/' + parent_file_name
    IMG_names = os.listdir(file)
    N_img = len(IMG_names)
    resize_scale = 1
    threshold_binarization = 8

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

    ### Cut image with resized scale ###
    cut_coords_list = list(cut_coords)
    x_1 = int(cut_coords_list[0] / resize_scale)
    x_2 = int(cut_coords_list[2] / resize_scale)
    y_1 = int(cut_coords_list[1] / resize_scale)
    y_2 = int(cut_coords_list[3] / resize_scale)
    img_crop = img_reference[y_1:(y_1 + y_2), x_1:(x_1 + x_2)]
    img_gray_ref = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

    ### Save ROI dimensions and define Canny parameters ###
    fps = 60
    Ny, Nx = img_gray_ref.shape
    FC_mm = 1 / Ny                  # Factor de Conversión pix -> mm
    threshold_01 = 70
    threshold_02 = 5
    gaussian_kernel_size = (5, 5)

    ### Auxiliar images of reference ###
    img_blur_ref = cv2.GaussianBlur(img_gray_ref, gaussian_kernel_size, 0)
    img_canned_ref = cv2.Canny(img_blur_ref, threshold_01, threshold_02)


    ### Se genera un operador similar a Dx sparse y un vector contador ###
    D = sparse_D(Ny)
    enumerate_array = np.arange(Ny)[::-1]
    # Midiendo tiempo inicial
    now = datetime.datetime.now()
    print('Hora de Inicio: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_init = time.time()

    ### Iteración de detección ###
    Z = []
    for i in range(1, N_img):
        img_i = cv2.imread(file + '/' + IMG_names[i])
        img_crop = img_i[y_1:(y_1 + y_2), x_1:(x_1 + x_2)]
        img_gray = cv2.subtract(img_gray_ref, cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY))
        img_blur = cv2.GaussianBlur(img_gray, gaussian_kernel_size, 0)
        img_canned = cv2.Canny(img_blur, threshold_01, threshold_02)
        #if i >= int(N_img * 0.8):
        #    plt.plot(img_canned[:, i])
        #    plt.imshow(img_canned)
        #    plt.show()
        Z_i = []
        for j in range(Ny):
            n = 0
            while n <len(img_canned[j, :]) - 1:
                if img_canned[j, n] != 0:
                    Z_i.append(n)
                    n = len(img_canned[j, :]) - 1
                elif n == len(img_canned[j, :]) - 2:
                    Z_i.append(Z_i[-1])
                n = n + 1
        Z.append(Z_i)
    one_vect = np.ones(N_img)
    Z = np.array(Z)

    # Midiendo tiempo final
    now = datetime.datetime.now()
    print('Hora de Término: ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    time_fin = time.time()
    print(str(time_fin - time_init) + ' seg')

    ### Definiendo espacio-temporal en numpy en pixeles y mm ##
    X = np.arange(Ny)
    X_mm = FC_mm * X - (FC_mm * X[-1] / 2) * np.ones(Ny)
    T = np.arange(N_img - 1)
    T_s = T / fps
    Z_mm = FC_mm * Z

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    np.savetxt(save_directory + '/X.txt', X, delimiter=',')
    np.savetxt(save_directory + '/X_mm.txt', X_mm, delimiter=',')
    np.savetxt(save_directory + '/T.txt', T, delimiter=',')
    np.savetxt(save_directory + '/T_s.txt', T_s, delimiter=',')
    np.savetxt(save_directory + '/Z.txt', Z, delimiter=',')
    np.savetxt(save_directory + '/Z_mm.txt', Z_mm, delimiter=',')


    ### Visualizacion del diagrama espacio-temporal  ###
    pcm = plt.pcolormesh(X_mm, T_s, Z_mm, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(save_directory + '/water_level.png', dpi=1000)
    plt.close()