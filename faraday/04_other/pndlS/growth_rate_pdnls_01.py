from back_process import *
if __name__ == "__main__":
    k = np.arange(0, 0.6, 0.002)
    sigma = np.arange(-0.1, 0.2, 0.002)
    mu = 0.1
    nu = 0.09
    N_x = len(k)
    N_y = len(sigma)
    x, y = np.meshgrid(k, sigma)
    F = y ** 2 + 2 * mu * y + mu ** 2 + nu ** 2 - 2 * nu * x ** 2 + x ** 4
    gammas_flat = np.arange(0, mu, 0.02)
    gamma_c = np.array([mu])
    gammas_pattern = np.arange(mu + 0.04, 0.4, 0.0401)

    #fig = plt.figure()
    #ax = fig.add_axes()
    cp_01 = plt.contour(k, sigma, F ** 0.5, gammas_flat, colors='k', linestyles='--', linewidths=2, zorder=10)
    cp_02 = plt.contour(k, sigma, F ** 0.5, gamma_c, colors='r', linestyles='solid', linewidths=2, zorder=10)
    cp_03 = plt.contour(k, sigma, F ** 0.5, gammas_pattern , colors='k', linestyles='solid', linewidths=2, zorder=10)

    fmt_01 = {}
    for l, s in zip(cp_01.levels, gammas_flat):
        fmt_01[l] = '$\gamma='+str(0.01*int(s * 100))+'$'

    fmt_02 = {}
    for l, s in zip(cp_02.levels, gamma_c):
        fmt_02[l] = '$\gamma_{c}='+str(0.01*int(s * 100))+'$'

    fmt_03 = {}
    for l, s in zip(cp_03.levels, gammas_pattern):
        fmt_03[l] = '$\gamma='+str(0.01*int(s * 100))+'$'

    plt.clabel(cp_01, inline=1, fmt=fmt_01, fontsize=12)
    plt.clabel(cp_02, inline=1, fmt=fmt_02, fontsize=12)
    plt.clabel(cp_03, inline=1, fmt=fmt_03, fontsize=12)
    plt.vlines(0.3, -0.1, 0.2, colors='r', alpha=0.3, linestyles='solid')
    plt.hlines(0, 0, 0.6, colors='r', alpha=0.3, linestyles='solid')

    plt.grid(linestyle='--', alpha=0.2, color='k')
    plt.xlim([0, 0.6])
    plt.ylim([-0.1, 0.2])
    plt.xlabel('$k$', size=25)
    plt.xticks(fontsize=15)

    plt.ylabel('$\\textrm{Re}(\sigma)$', size=25)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.savefig('new_growth.png', dpi=300)
    plt.close()