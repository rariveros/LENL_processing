import matplotlib.pyplot as plt

from directories import *
from back_process import *

if __name__ == '__main__':

    ###    Abriendo archivos    ###
    disco = 'D:'
    initial_dir_data = str(disco) + '/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    working_directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')
    directories = [d for d in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, d))]
    dist = 20
    GAMMA = []
    FREQ_L = []
    FREQ_L_STD = []
    PER_L = []
    FREQ_R = []
    FREQ_R_STD = []
    PER_R = []
    AMAX = []
    DT = []

    for dir in directories:
        directory = os.path.join(working_directory, dir)
        ampd = float(dir.split("_")[0].split("=")[-1])
        freq = float(dir.split("_")[1].split("=")[-1])
        d = float(dir.split("_")[2].split("=")[-1])
        alpha, beta, nu, gamma, f1 = fluid_pdnls_parameters(freq, ampd, dist)

        X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
        T = np.loadtxt(directory + '/T_strobo.txt', delimiter=',')
        Z = np.loadtxt(directory + '/Z_strobo.txt', delimiter=',')
        DT.append(T[1] - T[0])
        X0 = 5
        X = X - X0
        I0 = np.argmin(np.abs(X))
        Nx = len(X)

        pcm = plt.pcolormesh(X, T, Z, cmap=test_cm, shading='auto')
        cbar = plt.colorbar(pcm, shrink=1)
        cbar.set_label('$|A(x, t)|$', rotation=0, size=13, labelpad=-27, y=1.1)
        plt.xlabel('$x$', size='20')
        plt.ylabel('$t$', size='20')
        plt.grid(linestyle='--', alpha=0.5)
        plt.savefig(directory + "/centered_spatiotemporal.png", dpi=200)
        plt.close()

        ZL = integrate.simpson(Z[:, :I0], X[:I0], axis=1)
        ZR = integrate.simpson(Z[:, I0:], X[I0:], axis=1)
        plt.plot(T, ZL, color="r")
        plt.plot(T, ZR, color="b")
        plt.savefig(directory + "/timeseries_dimerized.png", dpi=200)
        plt.close()

        dt = T[1] - T[0]
        CCF_L = np.correlate(ZL - np.median(ZL), ZL - np.median(ZL), "full")
        CCF_R = np.correlate(ZR - np.median(ZR), ZR - np.median(ZR), "full")
        tau = np.arange(-T[-1], T[-1], dt)

        Ntau = len(tau)
        dtau = tau[1] - tau[0]

        CCF_max, tau_max, CCF_I = max_finder(CCF_L[:-1], tau, Ntau, dtau)
        plt.plot(tau, CCF_L[:-1])
        plt.scatter(tau_max, CCF_max)
        plt.savefig(directory + "/CCF.png", dpi=200)
        plt.close()
        tau_L = []
        maxval = np.amax(CCF_L)
        for j in range(len(tau_max)):
            if CCF_max[j] > 0.25 * maxval:
                tau_L.append(tau_max[j])
        if len(tau_L) != 1 and d != 12:
            freq_L = 1 / np.mean(np.diff(tau_L))
            freq_L_std = np.abs(np.std(np.diff(tau_L)) / np.mean(np.diff(tau_L)) ** 2)
        else:
            freq_L = 0
            freq_L_std = 0
        #### RIGHT ####
        CCF_max, tau_max, CCF_I = max_finder(CCF_R[:-1], tau, Ntau, dtau)
        tau_R = []
        maxval = np.amax(CCF_R)
        for j in range(len(tau_max)):
            if CCF_max[j] > 0.25 * maxval:
                tau_R.append(tau_max[j])
        if len(tau_R) != 1 and d != 12:
            freq_R = 1 / np.mean(np.diff(tau_R))
            freq_R_std = np.abs(np.std(np.diff(tau_R)) / np.mean(np.diff(tau_R)) ** 2)
        else:
            freq_R = 0
            freq_R_std = 0
        period_L = np.mean(np.diff(tau_L))
        period_R = np.mean(np.diff(tau_R))
        GAMMA.append(d + 31.6)
        FREQ_L.append(freq_L)
        PER_L.append(period_L)
        FREQ_L_STD.append(freq_L_std)
        FREQ_R.append(freq_R)
        PER_R.append(period_R)
        FREQ_R_STD.append(freq_R_std)
        AMAX.append(np.amax(Z))
    print(DT)
    GAMMA.append(11 + 31.6)
    FREQ_L.append(0)
    PER_L.append(0)
    FREQ_L_STD.append(0)
    FREQ_R.append(0)
    PER_R.append(0)
    FREQ_R_STD.append(0)
    AMAX.append(np.amax(Z))
    #FREQ[3] = 0
    plt.errorbar(GAMMA, 1000 * np.array(FREQ_L), FREQ_L_STD, ls='', ecolor="k", mec='black', color="k")
    plt.scatter(GAMMA, 1000 * np.array(FREQ_L), c="k")
    plt.errorbar(GAMMA, 1000 * np.array(FREQ_R), FREQ_R_STD, ls='', ecolor="k", mec='black', color="r")
    plt.scatter(GAMMA, 1000 * np.array(FREQ_R), c="k")
    plt.xlim(30, 50)
    plt.ylim(0, 100)
    plt.xlabel("$d\ (\\textrm{mm})$", fontsize=18)
    plt.ylabel("$f\ (\\textrm{mHz})$", fontsize=18)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.grid()
    plt.savefig(working_directory + "/freq.png", dpi=200)
    plt.close()

    plt.scatter(GAMMA, PER_L, c="k")
    plt.xlim(30, 45)
    plt.ylim(0, 1.1 * np.amax(PER_L))
    plt.xlabel("$d\ (\\textrm{mm})$", fontsize=18)
    plt.ylabel("$T$", fontsize=18)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.grid()
    plt.savefig(working_directory + "/period.png", dpi=200)
    plt.close()

    plt.scatter(GAMMA, AMAX, c="k")
    plt.xlim(30, 45)
    plt.ylim(0, 7)
    plt.xlabel("$d\ (\\textrm{mm})$", fontsize=18)
    plt.ylabel("$A_{max}\ (\\textrm{mm})$", fontsize=18)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.grid()
    plt.savefig(working_directory + "/amax.png", dpi=200)
    plt.close()

