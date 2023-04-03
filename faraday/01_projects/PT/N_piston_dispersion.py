from directories import *
from back_process import *
from back_faraday import *


if __name__ == "__main__":
    h = 20
    N_piston = 6
    m = 16
    n = 3

    freqs = dispersion_per_piston(h, N_piston, m, n)
    print_freqs(freqs, 5, 1)
    print_freqs(freqs, 8, 0)
    print_freqs(freqs, 9, 0)

    plt.savefig(str(N_piston) + '_piston_dispersion_relation.png', dpi=300)
    plt.close()