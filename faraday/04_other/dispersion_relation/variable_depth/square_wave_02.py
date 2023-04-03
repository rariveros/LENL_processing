from back_process import *

if __name__ == "__main__":
    x = np.arange(-20, 20, 0.01)
    Nx = len(x)
    y = np.zeros(Nx)

    n = 3
    injection_length = 20
    g = 9.81

    T = 2 * injection_length / n

    if n % 2 == 0:
        for i in range(Nx):
            if x[i] < - injection_length / 2 or x[i] > injection_length / 2:
                y[i] = 0
            else:
                y[i] = 2 * (2 * np.floor(x[i] / T) - np.floor(2 * x[i] / T)) + 1
    elif n % 2 == 1:
        for i in range(Nx):
            if x[i] < - injection_length / 2 or x[i] > injection_length / 2:
                y[i] = 0
            else:
                y[i] = 2 * (2 * np.floor((x[i] + T / 4) / T) - np.floor(2 * (x[i] + T / 4) / T)) + 1

    # The parametrized function to be plotted
    def f(y, wavelength):
        k = 2 * np.pi / wavelength
        y = np.sqrt(g * k * np.tanh(k * (2 - y)))
        return y

    # Define initial parameters
    init_wavelength = 4
    range = 4
    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    line, = plt.plot(x, f(y, init_wavelength), lw=2)
    plt.vlines(-10, ymin=0, ymax=10, colors='r', linestyles='--')
    plt.vlines(10, ymin=0, ymax=10, colors='r', linestyles='--')
    plt.xlim(x[0], x[-1])
    plt.ylim(np.amin(f(y, init_wavelength + range / 2)), np.amax(f(y, init_wavelength - range / 2)))
    plt.grid()
    ax.set_xlabel('Space [cm]')
    ax.set_xlabel('Frequency [Hz]]')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.25, bottom=0.25)

    # Make a horizontal slider to control the frequency.
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
    wavelength_slider = Slider(
        ax=axfreq,
        label='Wavelenght (cm)',
        valmin=init_wavelength - range / 2,
        valmax=init_wavelength + range / 2,
        valinit=init_wavelength,
    )

    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata(f(y, wavelength_slider.val))
        fig.canvas.draw_idle()


    # register the update function with each slider
    wavelength_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        wavelength_slider.reset()
    button.on_clicked(reset)

    plt.show()