from back_process import *


if __name__ == '__main__':
    l_x = 110.76
    d = 20
    a_ang = 7.4
    f_i = 14.86

    alpha, beta, nu, gamma = fluid_pdnls_parameters(f_i, a_ang, d)
    g = 9790
    l_y = 15
    w = 2 * np.pi * (f_i / 2)
    k_y = np.pi / l_y
    k_x, wavelength_x = wavelength_pattern(w, g, d, k_y)
    nu_02 = np.sqrt(k_x)
    print("----------FLUID----------")
    print("freq_iny =" + str(f_i))
    print("amp_ang =" + str(a_ang))

    print("----------PDNLS----------")
    print("A =" + str(alpha))
    print("B =" + str(beta))
    print("nu =" + str(nu))
    print("nu_2 =" + str(nu_02))
    print("gamma =" + str(gamma))
