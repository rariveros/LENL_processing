from back_process import *

if __name__ == '__main__':
    disc = 'E'
    Bs = genfromtxt(disc + ':/mnustes_science/simulation_data/tesis_rafael/Bs.txt', delimiter=',')
    deltas = genfromtxt(disc + ':/mnustes_science/simulation_data/tesis_rafael/deltas.txt', delimiter=',')
    deltas_dx = np.arange(0, 0.1, 0.0001)
    def F(x, A, n):
        return A * x ** n

    popt, pcov = curve_fit(F, deltas, Bs, bounds=(0, 10))
    A = popt[0]
    n = popt[1]
    print(A)
    print(n)

    B_fit = A * deltas_dx ** n

    plt.plot(deltas_dx, B_fit, c='r', linestyle='--')
    plt.scatter(deltas, Bs, c='k', zorder=3)
    plt.rc('axes', axisbelow=True)
    plt.grid(zorder=0)
    plt.xlabel('$\delta$', rotation=0, size=20)
    plt.ylabel('$B_0$', rotation=0, size=20, labelpad=15)
    plt.xlim([-0.0025, 0.0625])
    plt.ylim([0, 0.45])
    plt.savefig('E:/mnustes_science/simulation_data/tesis_rafael/power_law.png', dpi=300)
    plt.close()
