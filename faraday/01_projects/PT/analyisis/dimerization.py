from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'D:'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data/soliton_control/espacio_parametros/a=1_f=13.7'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_strobo.txt', delimiter=',')
    Z = np.loadtxt(directory + '/Z_strobo.txt', delimiter=',')
    X0 = 1
    X = X - X0
    I0 = np.argmin(np.abs(X))
    Nx = len(X)

    ZL = integrate.simpson(Z[:, :I0], X[:I0], axis=1)
    ZR = integrate.simpson(Z[:, I0:], X[I0:], axis=1)
    plt.plot(T, ZL, color="r")
    plt.plot(T, ZR, color="b")
    plt.show()