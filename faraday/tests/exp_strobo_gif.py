from directories import *
from back_process import *


if __name__ == "__main__":

    ### Definiendo parametros y eligiendo carpeta a detectar ###
    disco = 'D:'
    project_file = 'OSC'
    initial_dir_img = str(disco) + '/mnustes_science/images'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askdirectory(parent=root, initialdir=initial_dir_img, title='Elección de carpeta')
    parent_file_name = os.path.basename(file)
    save_directory = disco + '/mnustes_science/experimental_data/' + project_file + '/' + parent_file_name
    IMG_names = os.listdir(file)
    N_img = len(IMG_names)
    I_strobo_directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_img, title='Elección de carpeta')
    I_strobo = np.loadtxt(I_strobo_directory + '/I_stroboscopic.txt', delimiter=',')
    T_strobo = np.loadtxt(I_strobo_directory + '/T_stroboscopic.txt', delimiter=',')
    imgs_strobo = []
    for i_strobo in I_strobo:
        img_i = cv2.imread(file + '/' + IMG_names[int(i_strobo)])
        imgs_strobo.append(img_i)

    fig = plt.figure()
    im = plt.imshow(imgs_strobo[0], animated=True)
    plt.axis('off')

    def updatefig(i):
        im.set_array(imgs_strobo[i])
        plt.title("$t = " + str(T_strobo[i]).split(".")[0] + "." + str(T_strobo[i]).split(".")[1][0:1] + "\ \\textrm{s}$", fontsize=25)
        return im,


    ani = FuncAnimation(fig, updatefig, frames=len(I_strobo), interval=1, blit=True)
    ani.save("test_02.gif", dpi=300, writer=PillowWriter(fps=120))
