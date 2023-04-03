from directories import *
from back_process import *
from back_faraday import *


if __name__ == "__main__":
    x = np.arange(0, 2 * np.pi, 0.01)
    y = np.empty_like(x)

    m_1 = 25 / np.pi
    m_2 = - 10 / np.pi
    m_3 = 10 / np.pi

    gtr = np.pi / 180
    zero = 27

    for i in range(len(x)):
        if 0 <= x[i] < np.pi / 4:
            y[i] = 28
        elif np.pi / 4 <= x[i] < 5 * np.pi / 12:
            y[i] = float("NaN")
        elif 5 * np.pi / 12 <= x[i] < 11 * np.pi / 12:
            y[i] = m_2 * x[i] + 35
        elif 11 * np.pi / 12 <= x[i] < 13 * np.pi / 12:
            y[i] = float("NaN")
        elif 13 * np.pi / 12 <= x[i] < 19 * np.pi / 12:
            y[i] = m_3 * x[i] + 15
        elif 19 * np.pi / 12 <= x[i] < 7 * np.pi / 4:
            y[i] = float("NaN")
        elif 7 * np.pi / 4 <= x[i] < 2 * np.pi:
            y[i] = 28
    df = pd.DataFrame(y, columns=['a'])
    df = df.interpolate(method='polynomial', order=5)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_xticks(np.arange(0, 359, 15) * gtr)
    ax.plot(x, df)
    ax.plot(x, y, color='r')
    #ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)
    plt.show()

