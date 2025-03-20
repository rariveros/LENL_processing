from directories import *
from back_process import *

if __name__ == '__main__':
    periods = [[15.17, 15.32, 15.15, 15.06, 15.00],
               [12.90, 12.84, 13.99, 12.81, 12.53],
               [13.25, 13.67, 13.58, 13.35, 13.05],
               [14.91, 15.40, 15.43, 15.14, 15.23],
               [np.inf, np.inf, np.inf, np.inf, np.inf],
               [14.95, 14.32, 14.36, 15.18, 14.16],
               [14.16, 14.27, 14.61, 14.16, 14.16],
               [13.15, 13.55, 13.6, 14.01, 13.01]]
    amps = np.array([10.2, 10.0, 9.8, 9.6, 9.4, 10.4, 10.6, 10.8])
    period_mean = np.mean(np.array(periods), axis=1)
    plt.errorbar(amps, 1 / period_mean, yerr=np.abs(1 / period_mean ** 2) * np.std(periods, axis=1), marker='s', linestyle="", c="k")
    plt.show()