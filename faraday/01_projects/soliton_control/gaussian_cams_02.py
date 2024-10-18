from directories import *
from back_process import *
from back_faraday import *


if __name__ == "__main__":
    x = np.arange(0, 2 * np.pi, 0.01)
    y = np.empty_like(x)

    m_1 = 6 / np.pi
    m_2 = 12 / np.pi
    m_3 = 15 / np.pi

    gtr = np.pi / 180
    zero = 27

    for i in range(len(x)):
        if 0 * gtr <= x[i] < 45 * gtr:
            y[i] = m_1 * x[i] + zero
        elif 45 * gtr <= x[i] < 75 * gtr:
            y[i] = float("NaN")
        elif 75 * gtr <= x[i] < 165 * gtr:
            y[i] = m_2 * x[i] - m_2 * 120 * gtr + zero
        elif 165 * gtr <= x[i] < 195 * gtr:
            y[i] = float("NaN")
        elif 195 * gtr <= x[i] < 285 * gtr:
            y[i] = m_3 * x[i] - m_3 * 240 * gtr + zero
        elif 285 * gtr <= x[i] < 315 * gtr:
            y[i] = float("NaN")
        elif 315 * gtr <= x[i] < 360 * gtr:
            y[i] = m_1 * x[i] - m_1 * 360 * gtr + zero
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
