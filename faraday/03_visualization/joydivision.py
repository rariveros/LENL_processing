from directories import *
from back_process import *

from matplotlib.animation import FuncAnimation, PillowWriter

if __name__ == "__main__":
    disco = 'C'
    initial_dir_data = str(disco) + ':/Users/mnustes_science/PT_fluids/mnustes_scienc'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_mm_stroboscopic.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_stroboscopic.txt', delimiter=',')

    dt = 2
    t_init = 0
    N = 50
    Z = filtro_superficie(Z, 20, "X")
    px = 1 / plt.rcParams['figure.dpi']
    #fig1, ax1 = plt.subplots(figsize=(1200 * px, 1400 * px))
    #for n in range(0, N, 1):
    #    ax1.plot(X, np.real(C_mod[int(t_init + n * dt), :]) + n * 2, color=(1 - (n / N), 0, n / N, 0.5))

    fig2, ax2 = plt.subplots(figsize=(1200 * px, 1400 * px))
    for n in range(0, N, 1):
        ax2.plot(X, np.abs(Z[int(t_init + n * dt), :])/2 + n * 1, color=(1 - (n / N), 0, n / N, 0.95), lw=3, zorder=n)
        #ax2.plot(X, np.real(C_mod[int(t_init + n * dt), :]) + n * 0.5, color="k", linestyle="--", lw=2, alpha=0.85, zorder=n)
        ax2.set_xlim([X[0], X[-1]])
        plt.yticks([])
        ax2.set_xlabel('$x\ \\textrm{(mm)}$', fontsize=50)
        ax2.tick_params(labelsize=45)
        #plt.savefig('E:/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit', dpi=300)

    #fig3, ax3 = plt.subplots(figsize=(1200 * px, 1400 * px))
    #for n in range(0, N, 1):
    #    ax3.plot(X, np.abs(np.real(A[int(t_init + n * dt), :])) + n * 2, color=(1 - (n / N), 0, n / N, 0.5), zorder=n)
    plt.tight_layout()
    plt.savefig(directory + '/C_module.png', dpi=300)
    plt.close()

