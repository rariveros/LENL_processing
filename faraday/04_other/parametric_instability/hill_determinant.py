from back_process import *
from back_faraday import *

if __name__ == "__main__":
    N = 4
    damping = 0.17
    alpha = np.arange(0, 2, 0.01)
    beta = np.arange(0, 2, 0.01)
    N_alpha = len(alpha)
    N_beta = len(beta)
    Z_det = np.zeros((N_beta, N_alpha), dtype='complex_')
    for i in range(len(alpha)):
        print(str(i)+'/'+str(N_alpha))
        for j in range(len(beta)):
            Z_det[j, i] = hill_determinant_damping(alpha[i], beta[j], damping, N)
    #np.savetxt('Z_dets_damp_0.4.txt', Z_det, delimiter=',')
    #np.savetxt('alpha_dets_damp.txt', alpha, delimiter=',')
    #np.savetxt('beta_dets_damp.txt', beta, delimiter=',')
    #pcm = plt.pcolormesh(alpha, beta, np.abs(Z_det), cmap='Greys', shading='auto')
    #plt.contourf(alpha, beta, np.abs(Z_det), linestyles='solid')
    plt.contour(alpha, beta, np.real(Z_det), [0], colors='r', linestyles='solid')
    #plt.colorbar()
    plt.show()



