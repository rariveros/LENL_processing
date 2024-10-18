from directories import *
from back_process import *
from back_faraday import *


if __name__ == "__main__":
    xdata = [7.4, 7.3, 7.2, 7.1, 7.0, 6.9, 6.8, 6.7, 6.6, 6.5, 6.4, 6.3, 6.2, 6.1, 6.0, 5.9, 5.8, 5.7, 5.6, 5.5,
             5.4, 5.3, 5.2, 5.1]
    ydata = [3.6213, 3.5867, 3.4288, 3.3268, 3.3268, 3.2738, 3.2360, 3.2952, 3.2760, 3.0530, 3.0764, 3.0633,
             3.0354, 3.0299, 2.9261, 2.9450, 2.6772, 2.6471, 2.5554, 2.4726, 2.3293, 2.2570, 2.269, 2.163]
    for i in range(15):
        x_i = 5.0 - i * 0.1
        y_i = 0
        xdata.append(x_i)
        ydata.append(y_i)
    ampd = np.array(xdata)
    a_max = np.array(ydata)
    gamma = 8.401093 * 10 ** (-5) * ampd * 16.00 ** 2
    #plt.scatter(gamma, a_max)
    #plt.show()
    #plt.close()
    gamma_0 = 8.401093 * 10 ** (-5) * np.array(xdata) * 16.00 ** 2
    a_max_0 = ydata
    gamma_critico = 8.401093 * 10 ** (-5) * 5.0 * 16.00 ** 2

    def F(x, A, c, b):
        x = x.astype('complex128')
        return A * ((x - c) ** b)

    popt, pcov = curve_fit(F, gamma_0, a_max_0, bounds=[(8, gamma_critico, 0.2), (13, 0.11, 0.3)])
    A = popt[0]
    c = popt[1]
    b = popt[2]
    print(A)
    print(c)
    print(b)

    alpha, beta, nu, gamma_param = fluid_pdnls_parameters(16, 5, 2)
    sigma_i = 60
    mu_01 = (9 / (2 * np.sqrt(3))) * (A ** 4) / (alpha ** 2)
    mu_02 = c - np.sqrt(nu * alpha) / sigma_i
    print(mu_01)
    print(mu_02)


    gamma_fit = np.arange(c, 0.17, 0.00001)
    a_max_fit = F(gamma_fit, A, c, b)
    fig, ax = plt.subplots()
    textstr = '\n'.join((
        r'$A=%.3f$' % (A,),
        r'$\mathrm{\gamma_c}=%.3f$' % (c,),
        r'$\mathrm{\alpha}=%.4f$' % (b,)))

    plt.xlabel('$\gamma$', size=20)
    plt.ylabel('$A_{\\textrm{max}}\ \\textrm{(mm)}$', size=20)
    plt.scatter(gamma, a_max, c="k")
    plt.plot(gamma_fit, a_max_fit, '--', linewidth='2', c='r')
    plt.ylim([0, 4.5])
    plt.xlim([0.08, 0.16])
    #plt.legend(loc='best', fancybox=True, shadow=True)
    plt.grid(True, alpha=0.25)
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', bbox=props)
    plt.show()
    plt.close()