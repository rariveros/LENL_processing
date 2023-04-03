from directories import *
from back_process import *

if __name__ == "__main__":
    # %matplotlib inline
    helvetica = matplotlib.font_manager.FontProperties(
        fname=r"C:\Users\Rafael Riveros\AppData\Local\Programs\Python\Python310\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\Helvetica.ttf")
    print(str(helvetica.get_name()))
    # Plot the square wave
    t = np.linspace(0, 1, 1000, endpoint=True)
    plt.plot(t, signal.square(2 * np.pi * 5 * t))

    # Change the x, y axis label to "Brush Script MT" font style.
    plt.xlabel("Time (Seconds)", fontname="Brush Script MT", fontsize=18)
    plt.ylabel("Amplitude $f_i$", fontname="Helvetica", fontsize=18)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.show()