from back_process import *

if __name__ == "__main__":
    f = np.arange(0, 20, 0.01)
    angle = np.arange(-10, 30, 0.05)
    a = angle/12
    g = 9790
    h = 20
    l_x = 16
    l_y = 240
    kx = 1 * np.pi / l_x
    ky = 1 * np.pi / l_y
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega_1 = np.sqrt(g * k * np.tanh(k * h))
    f_1 = 2 * omega_1 / (2 * np.pi)
    x_f, y_angle = np.meshgrid(f, angle)
    mu = 0.22
    #Z = (4 * (y_angle / 12) / (4 * g)) ** 2 - mu ** 2 - (0.5 * ((x_f / f_1) ** 2 - 1)) ** 2
    Z = (4 * (y_angle / 12) * (np.pi * x_f) ** 2 / (4 * g)) ** 2 - mu ** 2 - (0.5 * ((x_f / f_1) ** 2 - 1)) ** 2
    Z_2 = (4 * (y_angle / 12) * (np.pi * x_f) ** 2 / (4 * g)) - mu
    #mu_vis = 0.1 * (5 * np.pi / l_y) ** 2#f_1 ** 2 * (0.5 * ((f_i / f_1) ** 2 - 1))
    #print(mu_vis)

    #(y_Gamma / (4 * g)) ** 2 - 0.15 ** 2 - (0.5 * ((x_f / f_1) ** 2 - 1)) ** 2
    def a_to_Gamma(x):
        return 6 * x / (np.pi ** 2)
    def Gamma_to_a(x):
        return np.pi ** 2 * x / 6

    fig1, ax1 = plt.subplots(1)
    cs_1 = plt.contour(f, angle, Z, [0], colors='b', linestyles='solid')
    plt.close()
    lines = []
    for line in cs_1.collections[0].get_paths():
        lines.append(line.vertices)

    fig2, ax2 = plt.subplots(1)
    cs_2 = plt.contour(f, angle, Z_2, [0], colors='b', linestyles='solid')
    plt.close()
    lines2 = []
    for line in cs_2.collections[0].get_paths():
        lines2.append(line.vertices)
    #fig, ax = plt.subplots()
    #ax.plot(lines[0][:, 0], lines[0][:, 1], c='k', zorder=10)
    secax = ax2.secondary_yaxis('right', functions=(a_to_Gamma,
                                                   Gamma_to_a))
    secax.tick_params(axis='y', labelsize=15)
    ax2.tick_params(axis='y', labelsize=15)
    plt.plot(Z, zorder=4)
    #ax.hlines(np.amin(lines[0][:, 1]), 10, 20, colors='r', linestyles='--', zorder=1)
    #ax.vlines(f_1, 0, 20, colors='r', linestyles='--', zorder=1)
    #plt.xlabel('$\omega$', size='25')
    #plt.xticks(fontsize=15)
    #plt.ylabel('$a$', size='25')
    #plt.yticks(fontsize=15)
    #ax.set_xlim([10, 20])
    #ax.set_ylim([0, 20])
    #plt.show()
    #plt.close()

    Z = ((((lines[0][:, 0] / 2) / (2 * np.pi)) ** 2) * (lines[0][:, 1] / 12) * 0.5)
    Z_2 = ((((lines2[0][:, 0] / 2) / (2 * np.pi)) ** 2) * (lines2[0][:, 1] / 12) * 0.5)
    plt.plot(lines[0][:, 0], Z, c='k', zorder=10, linewidth=2)
    #plt.plot(lines2[0][:, 0], Z_2, c='k', zorder=10, linewidth=2)
    plt.fill_between(lines[0][:, 0], Z, 0, where=lines[0][:, 0] >= f_1 - 0.01, color=(174/255, 156/255, 255/255, 0.7))
    plt.fill_between(lines[0][:, 0], Z, 0, where=lines[0][:, 0] <= f_1, color=(160/255, 255/255, 150/255, 0.7))
    plt.fill_between(lines[0][:, 0], Z, 0.9, color=(255/255, 150/255, 150/255, 0.7))
    #plt.hlines(0.265, 10, 20, colors='r', linestyles='--', zorder=1)
    plt.vlines(f_1, 0, 20, colors='r', linestyles='--', zorder=10, linewidth=2)
    plt.xlabel('$f_i$', size='30')
    plt.xticks(fontsize=15)
    plt.ylabel('$\Gamma_0$', size='30', rotation=90)
    plt.yticks(fontsize=15)
    plt.grid(linestyle='--', alpha=0.2, color='k')
    plt.tight_layout()
    plt.xlim([12, 17])
    plt.ylim(0.5, 0.9)
    plt.savefig('figures/parameter_space_02.png', dpi=300)
    plt.close()