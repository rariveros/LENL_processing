from directories import *
from back_process import *

if __name__ == "__main__":
    x_grid = np.arange(-15, 15, 0.01)
    y_grid = np.arange(0, 10, 0.01)
    X, Y = np.meshgrid(x_grid, y_grid)
    lamda = 1
    mu = 1.2
    k = 1
    theta_0 = 0
    a = 1
    b = 1

    Z = (4 / lamda) * np.arctan(np.exp((b * lamda * (k * X + mu * Y + np.sin(Y) + theta_0)) / np.sqrt(b * lamda * (mu ** 2 - a * k ** 2))))
    np.savetxt('test_tracker/field_01/Z.txt', Z, delimiter=',')
    np.savetxt('test_tracker/field_01/x_grid.txt', x_grid, delimiter=',')
    np.savetxt('test_tracker/field_01/y_grid.txt', y_grid, delimiter=',')

    ### Visualizacion del diagrama espacio-temporal  ###
    pcm = plt.pcolormesh(x_grid, y_grid, Z, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig('test_tracker/field_01/field.png', dpi=200)
    plt.close()