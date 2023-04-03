from back_process import *

if __name__ == "__main__":
    Y = np.loadtxt('beta_dets.txt', delimiter=',')
    X = np.loadtxt('alpha_dets.txt', delimiter=',')
    Z_1 = np.loadtxt('Z_dets.txt', delimiter=',', dtype=complex)
    Z_2= np.loadtxt('Z_dets_damp_0.1.txt', delimiter=',', dtype=complex)
    Z_3 = np.loadtxt('Z_dets_damp_0.2.txt', delimiter=',', dtype=complex)
    Z_4 = np.loadtxt('Z_dets_damp_0.3.txt', delimiter=',', dtype=complex)
    Z_5 = np.loadtxt('Z_dets_damp_0.4.txt', delimiter=',', dtype=complex)
    Z_6 = np.loadtxt('Z_dets_damp_0.5.txt', delimiter=',', dtype=complex)
    Z_7 = np.loadtxt('Z_dets_damp_0.6.txt', delimiter=',', dtype=complex)
    #Z_2 = np.loadtxt('F_isocronus.txt', delimiter=',')
    print(len(X))
    print(len(Y))
    ZZ_1 = np.zeros((len(Z_1[:, 0]), len(Z_1[0, :])))
    #ZZ_2 = np.zeros((len(Z_2[:, 0]), len(Z_2[0, :])))
    print(np.shape(Z_1))
    print(np.shape(ZZ_1))
    delta = 1
    for i in range(len(Y)):
        for j in range(len(X)):
            if Z_1[i, j] < 0:
                ZZ_1[i, j] = 1
    #for i in range(len(X)):
    #    for j in range(len(Y)):
    #        if Z_2[i, j] < 0:
    #            ZZ_2[i, j] = 1
    ZZ = ZZ_1 #+ ZZ_2
    for i in range(len(Y)):
        for j in range(len(X)):
            if ZZ[i, j] == 2:
                ZZ[i, j] = 1
    ZZ[0, 0] = 5
    pcm = plt.pcolormesh(X, Y, ZZ, cmap='Greys', shading='auto', zorder=0)
    plt.contour(X, Y, Z_1, [50000000000000000], colors='r', zorder=10)
    #plt.contour(X, Y, Z_2, [50000000000000000], colors='r', linestyles='dashed')
    plt.contour(X, Y, Z_3, [50000000000000000], colors='#FF5C5C', linestyles=':', zorder=5)
    #plt.contour(X, Y, Z_4, [50000000000000000], colors='r', linestyles='dashed')
    plt.contour(X, Y, Z_5, [50000000000000000], colors='#FF9191', linestyles='-.', zorder=5)
    #plt.contour(X, Y, Z_6, [50000000000000000], colors='r', linestyles='dashed')
    plt.contour(X, Y, Z_7, [50000000000000000], colors='#FFbcbc', linestyles='--', zorder=5)
    plt.xlim([0, 8])
    plt.ylabel('$\\beta$', fontsize=20)
    plt.xlabel('$\\alpha$', fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(alpha=0.4)
    plt.tight_layout()
    plt.savefig('mathieu_damp.png', dpi=300)
    plt.close()
    plt.show()