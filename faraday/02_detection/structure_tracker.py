from directories import *
from back_process import *


if __name__ == "__main__":
    test_directory = "C:/Users/research/LENL_processing/faraday/tests/test_tracker"

    mode = "fronts" #solitons or fronts

    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=test_directory, title='Elección de carpeta')
    parent_directory_name = os.path.basename(directory)

    root = tk.Tk()
    root.withdraw()
    reference_image = filedialog.askopenfilename(parent=root, initialdir=directory, title='Reference Selection')
    img_reference = cv2.imread(str(reference_image))

    Z = np.loadtxt(directory + '/Z.txt', delimiter=',')
    x_grid = np.loadtxt(directory + '/x_grid.txt', delimiter=',')
    y_grid = np.loadtxt(directory + '/y_grid.txt', delimiter=',')

    Nx = len(x_grid)
    Ny = len(y_grid)
    dx = x_grid[1] - x_grid[0]

    resize_scale = 1
    h, w, c = img_reference.shape
    h_resized, w_resized = h * resize_scale, w * resize_scale
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

    Ny_pix, Nx_pix = img_gray_ref.shape
    wind_R_pix, wind_L_pix = define_window(img_crop, resize_scale)
    wind_L_j = int((wind_L_pix / Nx_pix) * Nx)
    wind_R_j = int((wind_R_pix / Nx_pix) * Nx)
    delta_wind_0 = wind_R_j - wind_L_j
    if delta_wind_0 % 2 != 0:
        wind_R_j = wind_R_j + 1
    delta_wind_0 = wind_R_j - wind_L_j
    print(delta_wind_0)
    Z_windowed_0 = Z[0, wind_L_j:wind_R_j]
    N_window = len(Z_windowed_0)
    D = sparse_D(N_window, dx)
    DD = sparse_DD(N_window, dx)
    J = []
    I = []
    X_structure = []
    Y_structure = []
    Z_structure = []
    for i in range(Ny):
        if i != 0:
            wind_L_j = wind_L_j_new
            wind_R_j = wind_R_j_new
        Z_windowed_i = Z[i, wind_L_j:wind_R_j]
        if mode == "solitons":
            j_max_i = np.argmax(Z_windowed_i)
        elif mode == "fronts":
            DZ = Dx(D, Z_windowed_i)
            j_max_i = np.argmax(DZ)
        X_max_i = x_grid[wind_L_j + j_max_i]
        Y_max_i = y_grid[i]
        Z_max_i = Z[i, wind_L_j + j_max_i]
        J.append(j_max_i)
        I.append(i)
        X_structure.append(X_max_i)
        Y_structure.append(Y_max_i)
        Z_structure.append(Z_max_i)
        wind_L_j_new = int(wind_L_j + j_max_i - int(delta_wind_0 / 2))
        wind_R_j_new = int(wind_L_j + j_max_i + int(delta_wind_0 / 2))
    J = np.array(J)
    I = np.array(I)
    X_structure = np.array(X_structure)
    Y_structure = np.array(Y_structure)
    Z_structure = np.array(Z_structure)

    np.savetxt(directory + '/J.txt', J, delimiter=',')
    np.savetxt(directory + '/I.txt', I, delimiter=',')
    np.savetxt(directory + '/X_structure.txt', X_structure, delimiter=',')
    np.savetxt(directory + '/Y_structure.txt', Y_structure, delimiter=',')
    np.savetxt(directory + '/Z_structure.txt', Z_structure, delimiter=',')

    ### Visualizacion del diagrama espacio-temporal  ###
    pcm = plt.pcolormesh(x_grid, y_grid, Z, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.plot(X_structure, Y_structure, color="g")
    plt.savefig(directory + '/field_tracked.png', dpi=200)
    plt.close()








