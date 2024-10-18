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
    fun = df.to_numpy()
    plt.plot(fun)
    plt.ylim([0, 35])
    plt.show()
    plt.close()
    f_01 = []
    x_01 = []
    f_02 = []
    x_02 = []
    f_03 = []
    x_03 = []
    for i in range(len(x)):
        if 45 * gtr <= x[i] < 75 * gtr:
            f_01.append(fun[i][0])
            x_01.append(x[i])
        elif 165 * gtr <= x[i] < 195 * gtr:
            f_02.append(fun[i][0])
            x_02.append(x[i])
        elif 285 * gtr <= x[i] < 315 * gtr:
            f_03.append(fun[i][0])
            x_03.append(x[i])
    x_01 = np.array(x_01)
    f_01 = np.array(f_01)
    x_02 = np.array(x_02)
    f_02 = np.array(f_02)
    x_03 = np.array(x_03)
    f_03 = np.array(f_03)
    def poly(x, a, b, c, d, e, f):
        return a * x ** 0 + b * x ** 1 + c * x ** 2 + d * x ** 3 + e * x ** 4 + f * x ** 5
    popt_01, pcov = curve_fit(poly, x_01, f_01)
    popt_02, pcov = curve_fit(poly, x_02, f_02)
    popt_03, pcov = curve_fit(poly, x_03, f_03)
    array = [popt_01, popt_02, popt_03]
    print(np.array(array))
    plt.plot(f_01)
    plt.plot(poly(x_01, *popt_01))
    plt.plot(f_02)
    plt.plot(poly(x_02, *popt_02))
    plt.plot(f_02)
    plt.plot(poly(x_03, *popt_03))
    plt.show()