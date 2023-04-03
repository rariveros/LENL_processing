from directories import *
from back_process import *

from matplotlib.animation import FuncAnimation, PillowWriter

if __name__ == "__main__":
    disco = 'C'
    initial_dir_data = str(disco) + ':/Users/mnustes_science/PT_fluids/mnustes_science'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    Z = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')
    X = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T = np.loadtxt(directory + '/T_s.txt', delimiter=',')

    t_i = 3000
    t_f = 4000
    ratio = 3
    def animate(i):
        line.set_data(X, Z[i, :])
        return line,

    def init():
        line.set_data([], [])
        line.set_color('k')
        return line,

    fig = plt.figure()
    axis = plt.axes(xlim=(X[0], X[-1]),
                    ylim=(np.amin(Z), np.amax(Z)))
    plt.xlabel('$x\ \\textrm{(mm)}$', fontsize=20)
    plt.ylabel('$A_R(x)$', fontsize=20)
    plt.grid(alpha=0.4)
    axis.set_aspect(1)

    line, = axis.plot([], [], lw=2)

    ani = FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=70,
                                   interval=100,
                                   blit=True)
    #plt.show()
    ani.save("front.gif", dpi=300, writer=PillowWriter(fps=25))