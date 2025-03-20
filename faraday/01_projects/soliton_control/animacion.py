import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from scipy.signal import filtfilt
from back_process import *

if __name__ == "__main__":
    x =   np.loadtxt("D:\\mnustes_science\\experimental_data\\soliton_control\\espacio_parametros\\a=11.8_f=13.5_2\\X_mm.txt",delimiter=',')
    t =   np.loadtxt("D:\\mnustes_science\\experimental_data\\soliton_control\\espacio_parametros\\a=11.8_f=13.5_2\\T_s.txt",delimiter=',')
    z =   np.loadtxt("D:\\mnustes_science\\experimental_data\\soliton_control\\espacio_parametros\\a=11.8_f=13.5_2\\Z_mm.txt",delimiter=',')
    x_0 = np.loadtxt("D:\\mnustes_science\\experimental_data\\soliton_control\\espacio_parametros\\a=11.8_f=13.5_2\\IL_mm.txt",delimiter=',')

        ### filtro de grafica ###
        # window_size = 5
        # data_z = filtfilt(data_z)

        # Genera datos de ejemplo (reemplaza esto con tus datos)
    filas = 2001  # z= f,2001 c,1504
    columnas = 36
    data = z
    plt.show()


        # Función para actualizar el gráfico en cada fotograma de la animación
    def update(frame):
        plt.cla()  # Borra el gráfico anterior

        # Muestra los datos de la fila correspondiente al tiempo actual (frame)
        plt.plot(data[frame], marker='')

        # Personaliza el gráfico (etiquetas, límites, etc.) según tus necesidades
        plt.ylim([-10, 10])
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        plt.title(f'Frame {frame}')
        # plt.grid(True)


     # Crea la figura y la animación
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, frames=filas, interval=50)
    FFwriter = animation.FFMpegWriter(fps=10, metadata=dict(artist='Yo'), bitrate=1800)
    ani.save('ani_o_a=11.8_f=13.5.mp4', writer=FFwriter)
    print('guardando...')

    #Muestra la animación en una ventana
    #plt.show()
