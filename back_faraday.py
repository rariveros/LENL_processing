from back_process import *


def hill_determinant_isochornous(alpha, beta, N):
    N_array = np.arange(-N, N + 1)
    N = len(N_array)
    GAMMA = 2 * (alpha - N_array ** 2)
    data = np.ones((3, N))
    data[0] = beta
    data[1] = GAMMA
    data[-1] = beta
    diags = [1, 0, -1]
    hill_matrix = sparse.spdiags(data, diags, N, N)
    hill_matrix = sparse.lil_matrix(hill_matrix)

    hill_matrix = hill_matrix.toarray()
    hill_det = sp.linalg.det(hill_matrix)
    return hill_det


def hill_determinant_subarmonic(alpha, beta, N):
    N_array = np.arange(1, (int(N / 2) + 1))
    N_array = np.concatenate((np.flip(N_array), N_array))
    GAMMA = 2 * (alpha - 0.25 * (2 * N_array - np.ones(N)) ** 2)
    data = np.ones((3, N))
    data[0] = beta
    data[1] = GAMMA
    data[-1] = beta
    diags = [1, 0, -1]
    hill_matrix = sparse.spdiags(data, diags, N, N)
    hill_matrix = sparse.lil_matrix(hill_matrix)

    hill_matrix = hill_matrix.toarray()
    hill_det = sp.linalg.det(hill_matrix)
    return hill_det


def hill_determinant(alpha, beta, N):
    N_array = np.arange(-N, N + 1)
    N = len(N_array)
    GAMMA = 2 * (alpha - 0.25 * N_array ** 2)
    data = np.ones((3, N))
    data[0] = beta
    data[1] = GAMMA
    data[-1] = beta
    diags = [2, 0, -2]
    hill_matrix = sparse.spdiags(data, diags, N, N)
    hill_matrix = sparse.lil_matrix(hill_matrix)

    hill_matrix = hill_matrix.toarray()
    hill_det = sp.linalg.det(hill_matrix)
    return hill_det

def hill_determinant_damping(alpha, beta, damp, N):
    N_array = np.arange(-N, N + 1)
    N = len(N_array)
    GAMMA = 2 * (alpha + 0.5 * ((damp * N_array * 1j))- 0.25 * N_array ** 2)
    data = np.ones((3, N), dtype = 'complex_')
    data[0] = beta
    data[1] = GAMMA
    data[-1] = beta
    diags = [2, 0, -2]
    hill_matrix = sparse.spdiags(data, diags, N, N)
    hill_matrix = sparse.lil_matrix(hill_matrix)

    hill_matrix = hill_matrix.toarray()
    hill_det = sp.linalg.det(hill_matrix)
    return hill_det


def hill_test(alpha, beta, omega, mu, N):
    N_array = np.arange(-N, N + 1)
    N = len(N_array)
    gamma = 2 * (alpha + 0.5 * ((mu * N_array * 1j)) - omega ** 2 * N_array ** 2)
    data = np.ones((3, N), dtype='complex_')
    data[0] = beta
    data[1] = gamma
    data[-1] = beta
    diags = [2, 0, -2]
    hill_matrix = sparse.spdiags(data, diags, N, N)
    hill_matrix = sparse.lil_matrix(hill_matrix)

    hill_matrix = hill_matrix.toarray()
    hill_det = sp.linalg.det(hill_matrix)
    return hill_det

def dispersion_per_piston(h, N_piston, m_max, n_max):
    g = 9790
    L_x = (240 / 13) * N_piston
    L_y = 16
    colores = [[0.2422, 0.1504, 0.6603], [0.077, 0.7468, 0.7224], [0.9, 0.9, 0.0805]]
    markers = ['o', 'd', '^']
    freq_info = []

    fig, ax = plt.subplots()

    for n in range(0, n_max):
        m = np.arange(0, m_max)
        kx = m * np.pi / L_x
        ky = n * np.pi / L_y
        k = np.sqrt(kx ** 2 + ky ** 2)
        omega = np.sqrt(g * k * np.tanh(k * h))
        freq = 2 * omega / (2 * np.pi)
        freq_info.append(freq.tolist())
        #print("(" + str(n) + ", " + str(n) + ") = " + str(freq / 2) + ")")
        ax.scatter(m, omega, s=40, color=colores[n], marker=markers[n], label='$n_y = ' + str(n) + '$', zorder=10)
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
    return np.array(freq_info)


def print_freqs(freqs, m, n):
    print("Mode (" + str(m) + ", " + str(n) + "): " + r'f_i = %.3f' % (freqs[n, m],) + " Hz")