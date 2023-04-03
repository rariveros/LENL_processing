from back_process import *

if __name__ == "__main__":
    g = 9790
    h = 10
    #L_x = 26
    #L_y = 500
    L_x = 15
    L_y = 240
    colores = [[0.2422, 0.1504, 0.6603], [0.077, 0.7468, 0.7224], [0.9, 0.9, 0.0805]]
    markers = ['o', 'd', '^']

    def x_1_to_x_2(x):
        return np.pi * x


    def x_2_to_x_1(x):
        return x / (np.pi)


    fig, ax = plt.subplots()

    for i in range(0, 3):
        kx = i * np.pi / L_x
        n = np.arange(0, 16)
        ky = n * np.pi / L_y
        k = np.sqrt(kx ** 2 + ky ** 2)
        omega = np.sqrt(g * k * np.tanh(k * h))
        freq = 2 * omega / (2 * np.pi)
        print("(" + str(n) + ", " + str(i) + ") = " + str(freq) + ")")
        ax.scatter(n, omega, s=40, c=colores[i], marker=markers[i], label='$n_y = ' + str(i) + '$', zorder=10)
    ax.legend(fontsize=20)
    secax_y2 = ax.secondary_yaxis(1, functions=(x_2_to_x_1, x_1_to_x_2), zorder=12)
    secax_y2.set_ylabel("$f_i\ \\textrm{(Hz)}$", fontsize=25)
    secax_y2.tick_params(labelsize=18)
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 70])
    ax.set_xlabel('$n_x$', fontsize=30)
    ax.set_ylabel('$\omega\ \\textrm{(Hz Rad}^{-1})$', fontsize=25)
    plt.grid(alpha=0.3, zorder=0)
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], fontsize=18, zorder=12)
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70], fontsize=18)
    plt.tight_layout()
    plt.savefig('dispersion_relation_PUCV_10mm.png', dpi=300)
    plt.close()