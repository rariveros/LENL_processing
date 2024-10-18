from directories import *
from back_process import *
from back_faraday import *

if __name__ == "__main__":
    amps = np.array([8.5, 9.2, 9.9, 10.6, 11.3, 12.0])
    d = 20
    g = 9790
    f_ref = 13.8
    alpha, beta, nu, gamma, f0 = fluid_pdnls_parameters(f_ref, amps, d)
    print(f0)
    f_medidas = np.arange(13.8, 12.5, -0.1)
    alpha, beta, nus_scatter, gamma_med, f0_med = fluid_pdnls_parameters(f_medidas, 10, d)
    Dnu = np.abs(nus_scatter[-1] - nus_scatter[-2])
    nus = np.arange(nus_scatter[-1] - Dnu, nus_scatter[0] + Dnu, 0.001)
    F = f0 * (2 * nus + 1) ** 0.5
    F_scatter = f0 * (2 * nus_scatter + 1) ** 0.5

    for i in range(len(gamma)):
        A = gamma[i] / (F ** 2 * 8.401093 * 10 ** (-5))
        A_scatter = gamma[i] / (F_scatter ** 2 * 8.401093 * 10 ** (-5))
        plt.plot(F, A)
        plt.scatter(F_scatter, A_scatter, c="k", zorder=10)
    plt.xlabel('$f_i\ \\textrm{(Hz)}$', fontsize=22)
    plt.ylabel('$a_0$', fontsize=22)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlim(12.4, 13.9)
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig('f_a.png', dpi=200)
    plt.close()

    for i in range(len(gamma)):
        plt.plot([nus[-1], nus[0]], [gamma[i], gamma[i]])
        plt.scatter(nus_scatter, gamma[i] * np.ones(len(nus_scatter)), c="k", zorder=10)
    plt.xlabel('$\\nu$', fontsize=22)
    plt.ylabel('$\gamma_0$', fontsize=22)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlim(nus[0], nus[-1])
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig('nu_gamma.png', dpi=200)
    plt.close()

    for i in range(len(F_scatter)):
        A_i = gamma / (F_scatter[i] ** 2 * 8.401093 * 10 ** (-5))
        np.savetxt(str(F_scatter[i])[0:5] + '.txt', A_i, delimiter=',')

