from back_process import *

if __name__ == '__main__':
    gammas_np = genfromtxt(
        'E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/gammas.csv',
        delimiter=',')
    velocities_np = genfromtxt(
        'E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/velocities.csv',
        delimiter=',')
    velocities_error_np = genfromtxt(
        'E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/velocities_err.csv',
        delimiter=',')
    freq_np = genfromtxt(
        'E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/freq_processed/freq.csv',
        delimiter=',')
    freq_error_np = genfromtxt(
        'E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/freq_processed/freq_err.csv',
        delimiter=',')
    f_i = 14.80
    gammas_np = gamma_correction(gammas_np, f_i)


    def f_freq(x, A, c):
        x = x.astype('complex128')
        return A * np.abs((x - c) ** 0.5)


    def f(x, A, c, noise):
        x = x.astype('complex128')
        return A * (np.abs(((x - c) + (np.abs((x - c)) ** 2 + 2 * noise) ** 0.5) / 2)) ** 0.5


    def linear_fit(x, m, n):
        return m * x + n

    popt, pcov = curve_fit(f, gammas_np, velocities_np, bounds=[(0, 0.15, 0), (10, 0.25, 1)])
    popt_02, pcov = curve_fit(f_freq, gammas_np, velocities_np, bounds=[(0, 0.15), (10, 0.25)])

    A = popt[0]
    c = popt[1]
    noise = popt[2]
    A_02 = popt_02[0]
    c_02 = popt_02[1]

    print('A='+str(A_02))
    print('c=' + str(c_02))
    print('A_noise='+str(A))
    print('c_noise=' + str(c))
    print('noise=' + str(noise))

    cut = 15
    gammas_log = np.log(gammas_np[cut:-1] - c * np.ones(len(gammas_np[cut:-1])))
    #print(gammas[cut])
    velocities_log = np.log(velocities_np[cut:-1])
    velocities_error_log = velocities_error_np[cut:-1] / velocities_np[cut:-1]

    popt, pcov = curve_fit(linear_fit, gammas_log, velocities_log)
    m = popt[0]
    n = popt[1]
    x_grid_log = np.arange(gammas_log[0] - np.abs(gammas_log[0] - gammas_log[1]), gammas_log[-1] + np.abs(gammas_log[0] - gammas_log[1]), 0.01)
    velocities_log_fit = m * x_grid_log + n
    print("m =" + str(m))
    print("n =" + str(n))

    popt, pcov = curve_fit(linear_fit, gammas_np, freq_np)
    m_zz = popt[0]
    n_zz = popt[1]
    x_grid_log = np.arange(gammas_log[0] - np.abs(gammas_log[0] - gammas_log[1]), gammas_log[-1] + np.abs(gammas_log[0] - gammas_log[1]), 0.01)
    zz_log_fit = m_zz * x_grid_log + n_zz
    print("m_zz =" + str(m_zz))
    print("n_zz =" + str(n_zz))

    x_grid = np.arange(0.19, 0.26, 0.0005)
    velocity_noisy_fitted = []
    for i in range(len(x_grid)):
        epsilon_i = x_grid[i] - c
        velocity_noisy_fitted_i = A * ((epsilon_i + (epsilon_i ** 2 + 2 * noise) ** 0.5) / 2) ** 0.5
        velocity_noisy_fitted.append(velocity_noisy_fitted_i)
    velocity_noisy_fitted_np = np.array(velocity_noisy_fitted)

    x_grid_antierror = np.arange(c, 1, 0.0005)
    velocity_fitted = []
    for i in range(len(x_grid_antierror)):
        epsilon_i = x_grid_antierror[i] - c
        velocity_fitted_i = A * (epsilon_i) ** 0.5
        velocity_fitted.append(velocity_fitted_i)
    velocity_fitted_np = np.array(velocity_fitted)


    freq_zz = m_zz * x_grid + n_zz

    px = 1/plt.rcParams['figure.dpi']
    fig, ax1 = plt.subplots(figsize=(1200*px, 1000*px))
    ax1.set_xlabel('$\gamma\'_0$', fontsize=40)
    ax1.set_ylabel('$\langle v \\rangle\ \\textrm{(mm/s)}$', fontsize=40)
    ax1.tick_params(labelsize=30)
    ax1.errorbar(gammas_np, velocities_np, yerr=velocities_error_np, marker='o', ls='', markersize=8, capsize=5, capthick=1.5, ecolor='k', color='k', zorder=3)
    #ax1.plot(x_grid_antierror, velocity_fitted_np, linestyle='dotted', linewidth='3', c='r', label='Noise included',
    #         zorder=1)
    #ax1.plot(x_grid, velocity_noisy_fitted_np, '-', linewidth='3', c='r', label='No noise', zorder=2)
    ax1.set_ylim([0, 1])
    ax1.set_xlim([0.193, 0.25])

    ax1.grid(True)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit_dots',
                dpi=300)
    plt.close()

    fig, ax1 = plt.subplots(figsize=(1200*px, 1000*px))
    ax1.set_xlabel('$\gamma\'_0$', fontsize=40)
    ax1.set_ylabel('$\langle v \\rangle\ \\textrm{(mm/s)}$', fontsize=40)
    ax1.tick_params(labelsize=30)
    ax1.errorbar(gammas_np, velocities_np, yerr=velocities_error_np, marker='o', ls='', markersize=8, capsize=5, capthick=1.5, ecolor='k', color='k', zorder=3)
    #ax1.plot(x_grid_antierror, velocity_fitted_np, linestyle='dotted', linewidth='3', c='r', label='Noise included',
    #         zorder=1)

    ax1.plot(x_grid, velocity_noisy_fitted_np, '-', linewidth='4', c='r', label='No noise', zorder=2)
    ax1.set_ylim([0, 1])
    ax1.set_xlim([0.193, 0.25])

    ax1.grid(True)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit_dotsnoise',
                dpi=300)
    plt.close()

    fig, ax1 = plt.subplots(figsize=(1200*px, 1000*px))
    ax1.set_xlabel('$\gamma\'_0$', fontsize=40)
    ax1.set_ylabel('$\langle v \\rangle\ \\textrm{(mm/s)}$', fontsize=40)
    ax1.tick_params(labelsize=30)
    ax1.errorbar(gammas_np, velocities_np, yerr=velocities_error_np, marker='o', ls='', markersize=8, capsize=5, capthick=1.5, ecolor='k', color='k', zorder=3)
    ax1.plot(x_grid_antierror, velocity_fitted_np, linestyle='dotted', linewidth='4', c='r', label='Noise included',
             zorder=1)

    ax1.plot(x_grid, velocity_noisy_fitted_np, '-', linewidth='4', c='r', label='No noise', zorder=2)
    ax1.set_ylim([0, 1])
    ax1.set_xlim([0.193, 0.25])
    textstr_01 = '\n'.join((r'$A=%.2f$' % (A,) + "$\ \\textrm{mm/s}$", r'$\xi=%.3f$' % (noise * 10000,) + "$\\times 10^{-5}$", r"$\gamma_{D}'=%.3f$" % (c,)))
    props = dict(boxstyle='round', facecolor='whitesmoke', alpha=1)
    ax1.text(0.1, 0.65, textstr_01, transform=ax1.transAxes, fontsize=35, verticalalignment='top', bbox=props)

    ax1.grid(True)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit_velocities',
                dpi=300)
    plt.close()

    px = 1/plt.rcParams['figure.dpi']
    fig, ax1 = plt.subplots(figsize=(1200*px, 1000*px))
    ax1.set_xlabel('$\gamma\'_0$', fontsize=40)
    ax1.set_ylabel('$\langle v \\rangle\ \\textrm{(mm/s)}$', fontsize=40)
    ax1.tick_params(labelsize=30)
    ax1.errorbar(gammas_np, velocities_np, yerr=velocities_error_np, marker='o', ls='', markersize=7, capsize=5, capthick=1.5, ecolor='k', color='k', zorder=3)
    ax1.plot(x_grid_antierror, velocity_fitted_np, linestyle='dotted', linewidth='3', c='r', label='Noise included',
             zorder=1)

    ax1.plot(x_grid, velocity_noisy_fitted_np, '-', linewidth='3', c='r', label='No noise', zorder=2)
    ax1.set_ylim([0, 1])
    ax1.set_xlim([0.193, 0.25])
    textstr_01 = '\n'.join((r'$A=%.3f$' % (A,) + "$\ \\textrm{mm/s}$", r'$\xi=%.3f$' % (noise * 10000,) + "$\\times 10^{-5}$", r"$\gamma_{D}'=%.3f$" % (c,)))
    props = dict(boxstyle='round', facecolor='whitesmoke', alpha=1)
    ax1.text(0.7, 0.25, textstr_01, transform=ax1.transAxes, fontsize=25, verticalalignment='top', bbox=props)

    ax1.grid(True)

    left, bottom, width, height = [0.25, 0.6, 0.2, 0.3]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.plot(x_grid_log, velocities_log_fit, linestyle='--', linewidth='3', c=[1, 0., 0.], label='No noise', zorder=2)
    ax2.errorbar(gammas_log, velocities_log, yerr=velocities_error_log, marker='o', ls='', lw=1, ms=4, capsize=2, capthick=1, ecolor='k', color='k', zorder=3)
    ax2.tick_params(labelsize=20)
    plt.xlim([-6.01, -3.5])
    plt.xticks([-6, -5, -4])
    ax2.set_ylim([-1.5, 0])
    ax2.grid(True)
    ax2.set_xlabel('$\ln\Delta_D$', fontsize=25)
    ax2.set_ylabel('$\ln\langle v \\rangle$', fontsize=25)
    textstr_02 = "$\ln \langle v \\rangle = a \ln\Delta_D + b$"
    ax2.text(0.06, 0.95, textstr_02, transform=ax2.transAxes, fontsize=18, verticalalignment='top', zorder=0)
    textstr_01 = '\n'.join((r'$a=%.3f$' % (m,), r'$b=%.3f$' % (n,)))
    props = dict(boxstyle='round', facecolor='whitesmoke', alpha=1)
    ax2.text(0.55, 0.30, textstr_01, transform=ax2.transAxes, fontsize=15, verticalalignment='top', bbox=props)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit',
                dpi=300)
    plt.close()

    fig, ax = plt.subplots(figsize=(600*px, 500*px))
    textstr = '\n'.join((r'$a=%.3f$' % (m,), r'$b=%.3f$' % (n,)))
    textstr_02 = "$\ln \langle v \\rangle = a \ln\Delta_D + b$"
    plt.plot(x_grid_log, velocities_log_fit, linestyle='--', linewidth='2', c=[1, 0., 0.], label='No noise', zorder=2)
    plt.errorbar(gammas_log, velocities_log, yerr=velocities_error_log, marker='o', ls='', lw=1, ms=4, capsize=2,
                 capthick=1,
                 ecolor='k', color='k', zorder=3)
    plt.tick_params(labelsize=15)
    plt.grid(True)
    props = dict(boxstyle='round', facecolor='whitesmoke', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=17, verticalalignment='top', bbox=props)
    plt.xlim([-6.01, -3.5])
    plt.xlabel('$\ln\Delta_D$', fontsize=25)
    plt.ylabel('$\ln\langle v \\rangle$', fontsize=25)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/log-log',
                dpi=300)
    plt.close()

    fig, ax = plt.subplots()
    #textstr = '\n'.join((r'$a=%.3f$' % (m,), r'$b=%.3f$' % (n,)))
    #textstr_02 = "$\ln \langle v \\rangle = a \ln\Delta_D + b$"
    plt.plot(x_grid, freq_zz, linestyle='--', linewidth='3', c=[1, 0., 0.], label='No noise', zorder=2)
    plt.errorbar(gammas_np, freq_np, yerr=freq_error_np, marker='o', ls='', lw=1, ms=4, capsize=2,
                 capthick=1,
                 ecolor='k', color='k', zorder=3)
    plt.tick_params(labelsize=15)
    plt.grid(True)
    #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=20, verticalalignment='top', bbox=props)
    plt.xlim([0.1935, 0.25])
    plt.ylim([0, 0.35])
    plt.xlabel('$\gamma\'_0$', fontsize=25)
    plt.ylabel('$f_{zz}$', fontsize=25)
    plt.tight_layout()
    plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/ZZ',
                dpi=300)
    plt.close()