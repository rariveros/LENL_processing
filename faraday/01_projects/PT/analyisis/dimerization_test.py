from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'D:'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_strobo.txt', delimiter=',')
    Z = np.loadtxt(directory + '/Z_strobo.txt', delimiter=',')

    X0 = 1.4
    X = X - X0
    I0 = np.argmin(np.abs(X))
    Nx = len(X)

    pcm = plt.pcolormesh(X, T, Z, cmap=test_cm, shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$|A(x, t)|$', rotation=0, size=13, labelpad=-27, y=1.1)
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.show()
    plt.close()

    ZL = integrate.simpson(Z[:, :I0], X[:I0], axis=1)
    ZR = integrate.simpson(Z[:, I0:], X[I0:], axis=1)
    plt.plot(T, ZL, color="r")
    plt.plot(T, ZR, color="b")
    plt.show()
    plt.close()

    dt = T[1] - T[0]
    CCF = np.correlate(ZL - np.median(ZL), ZL - np.median(ZL), "full")
    tau = np.arange(-T[-1], T[-1], dt)

    Ntau = len(tau)
    dtau = tau[1] - tau[0]

    CCF_max, tau_max, CCF_I = max_finder(CCF[:-1], tau, Ntau, dtau)
    plt.plot(tau, CCF[:-1])
    plt.scatter(tau_max, CCF_max)
    plt.show()
    plt.close()
    tau_R = []
    maxval = np.amax(CCF)
    for j in range(len(tau_max)):
        if CCF_max[j] > 0.25 * maxval:
            tau_R.append(tau_max[j])
    if len(tau_R) == 1:
        freq = 0
        freq_std = 0
    else:
        freq = 1 / np.mean(np.diff(tau_R))
        freq_std = np.abs(np.std(np.diff(tau_R)) / np.mean(np.diff(tau_R)) ** 2)
    print(np.mean(np.diff(tau_R)), freq, freq_std)


