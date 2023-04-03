from back_process import *

if __name__ == '__main__':
    ampd = '13.5'

    ###   OPEN FILES   ###
    print('Abriendo archivos...')
    datos_path = 'F:/mnustes_science/experimental_data'
    carpeta = select_directory(datos_path)
    info_drift = genfromtxt(carpeta + '/dvelocities_info/info_dvelocity_' + ampd + '.csv', delimiter=',')
    fits = genfromtxt(carpeta + '/dvelocities_info/inputs/fits_dvelocity_' + ampd +'.csv', delimiter=',')
    print('Archivos Cargados (=^ ◡ ^=)')
    t_np = fits[0][0]
    x_np = fits[1][0]
    x_fit = fits[2][0]
    print(x_fit)


    x_fit_mm = x_np - x_fit[0]
    plt.scatter(t_np[0:-1:20], x_fit_mm[0:-1:20], c='k')
    plt.plot(t_np, x_fit_mm, c='k')
    plt.xlim([x_fit_mm[0], x_fit_mm[-1]])
    plt.xlabel('$t$', size='25')
    plt.xticks(fontsize=15)
    plt.ylabel('$$', size='25')
    plt.yticks(fontsize=15)
    plt.grid(linestyle='--', alpha=0.2, color='k')
    plt.tight_layout()
    plt.show()
    plt.close()
