from back_process import *
from back_faraday import *

if __name__ == "__main__":
    N = 10
    h = 20
    g = 9790
    L_x_0 = 111
    L_x_1 = 111
    L_y = 16
    f = np.arange(13, 17, 0.05)
    omega = np.pi * f
    a = np.arange(0, 4000, 50)
    Zs = []
    Ns = []
    ms0 = [6, 7, 8, 9, 10]
    ms1 = [1, 2, 3, 4, 5, 6]
    for m in ms0:
        n = 0
        kx = m * np.pi / L_x_0
        ky = n * np.pi / L_y
        k = np.sqrt(kx ** 2 + ky ** 2)
        mu = 4500 * k ** 2
        alpha = g * k * np.tanh(k * h)
        beta = a * k * np.tanh(k * h)
        N_omega = len(omega)
        N_beta = len(beta)
        Z_det = np.zeros((N_beta, N_omega), dtype='complex_')
        for i in range(len(omega)):
            if i % 100 == 0:
                print(str(i)+'/'+str(N_omega))
            for j in range(len(beta)):
                Z_det[j, i] = hill_test(alpha, beta[j], omega[i], mu,  N)
        Zs.append(Z_det)
        Ns.append(n)
    for m in ms1:
        n = 1
        kx = m * np.pi / L_x_1
        ky = n * np.pi / L_y
        k = np.sqrt(kx ** 2 + ky ** 2)
        mu = 4500 * k ** 2
        alpha = g * k * np.tanh(k * h)
        beta = a * k * np.tanh(k * h)
        N_omega = len(omega)
        N_beta = len(beta)
        Z_det = np.zeros((N_beta, N_omega), dtype='complex_')
        for i in range(len(omega)):
            if i % 100 == 0:
                print(str(i)+'/'+str(N_omega))
            for j in range(len(beta)):
                Z_det[j, i] = hill_test(alpha, beta[j], omega[i], mu,  N)
        Zs.append(Z_det)
        Ns.append(n)

    for i in range(len(Ns)):
        if Ns[i] == 0:
            c = "b"
        elif Ns[i] == 1:
            c = "r"
        plt.contour(f, a / g, np.real(Zs[i]), [0.001], colors=c, linestyles='solid')
    plt.title("$\\textrm{Arnol'd Tongues}$", size='15')

    plt.xlabel('$f_i\ (\\textrm{Hz})$', size='25')
    plt.xticks(fontsize=15)

    plt.ylabel('$a/g$', size='25')
    plt.yticks(fontsize=15)

    plt.grid(linestyle='--', alpha=0.2, color='k')
    plt.tight_layout()
    plt.savefig('hill_determinant_PUCV.png', dpi=300)
    plt.close()






