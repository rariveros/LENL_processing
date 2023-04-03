from back_process import *

if __name__ == "__main__":
    alpha = np.loadtxt('alpha_dets_damp.txt', delimiter=',')
    beta = np.loadtxt('beta_dets_damp.txt', delimiter=',')
    Z_det = np.loadtxt('Z_dets_damp_0.4.txt', dtype=complex, delimiter=',')
    N_alpha = len(alpha)
    N_beta = len(beta)
    Z_final = np.zeros((N_beta, N_alpha))
    #Z_det = np.abs(np.real(Z_det)) + np.abs(np.imag(Z_det))
    #for j in range(N_alpha):
    #    for i in range(N_beta):
    #        if Z_det[i, j] < 0.2 * 10e18:
    #            Z_final[i, j] = 1
    #Z_final[0, 0] = 2
    #for j in range(N_alpha):
    #    for i in range(N_beta):
    #        if Z_det[i, j] < 0.1 * 10e18:
    #            Z_det[i, j] = 0.0
    Z_final[0, 0] = 2
    #pcm = plt.pcolormesh(alpha, beta, np.imag(Z_det), shading='auto')
    plt.contour(alpha, beta, np.real(Z_det), [0], colors='r', linestyles='solid')
    #plt.xlim([0, 8])
    plt.grid(linestyle='solid')
    plt.xlabel('$\\alpha$')
    plt.ylabel('$\\beta$')
    plt.savefig('arnold_mathieu.png', dpi=300)
    plt.show()


