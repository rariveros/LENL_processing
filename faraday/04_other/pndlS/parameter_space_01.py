from back_process import *

if __name__ == "__main__":
    gamma = np.arange(0, 1, 0.01)
    nu = np.arange(-1, 1, 0.01)
    mu = 0.15
    nu_p = np.arange(0, 1, 0.01)
    nu_n = np.arange(-1, 0.01, 0.01)
    N_gamma = len(gamma)
    N_nu = len(nu)
    x_nu, y_gamma = np.meshgrid(nu, gamma)
    F = y_gamma ** 2 - mu ** 2
    G = x_nu ** 2

    plt.fill_between(nu_p, np.sqrt(nu_p ** 2 + mu ** 2), mu, color=(174/255, 156/255, 255/255, 0.7))
    plt.fill_between(nu_n, np.sqrt(nu_n ** 2 + mu ** 2), mu, color=(160/255, 255/255, 150/255, 0.7))
    plt.fill_between(nu, np.sqrt(nu ** 2 + mu ** 2), 1, color=(255/255, 150/255, 150/255, 0.7))
    plt.fill_between(nu, mu * np.ones(len(nu)), 0, color=(255/255, 250/255, 135/255, 0.7))
    plt.fill_between(mu * np.ones(len(gamma)), gamma)
    plt.contour(nu, gamma, G - F, [0], colors='k', linestyles='solid', linewidths=2, zorder=10)
    plt.contour(nu, gamma, y_gamma - mu, [0], colors='k', linestyles='solid', linewidths=2, zorder=10)
    plt.vlines(0, 0, 1, colors='r', linestyles='--', zorder=11, linewidth=2)


    plt.xlabel('$\\nu$', size='30')
    plt.xticks(fontsize=15)
    plt.ylabel('$\gamma_0$', size='30', rotation=90)
    plt.yticks(fontsize=15)
    plt.grid(linestyle='--', alpha=0.2, color='k')
    plt.xlim([-0.5, 0.5])
    plt.ylim([gamma[0], 0.6])
    plt.tight_layout()
    plt.savefig('figures/parameter_space_01.png', dpi=300)
    plt.close()