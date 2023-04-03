from directories import *
from back_process import *


if __name__ == "__main__":
    fs = 2000
    t_grid = np.arange(0, 1, 1 / fs)
    freq_01 = 40
    freq_02 = 8
    freq_00 = 10
    signal = chirp(t_grid, freq_00, t_grid[-1], freq_01 + freq_00)
    signal *= (1.0 + 0.5 * np.sin(2.0 * np.pi * 3.0 * t_grid))
    analytical_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytical_signal)
    instantaneous_phase = np.unwrap(np.angle(analytical_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /
                               (2.0 * np.pi) * fs)
    def F(x, m, n):
        return m * x + n

    popt, pcov = curve_fit(F, t_grid[1:], instantaneous_frequency)
    m = popt[0]
    n = popt[1]

    print(m)
    print(n)
    freq_real = freq_01 * t_grid[1:] + freq_00


    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.plot(t_grid, signal, label='Real signal', color='k')
    ax0.plot(t_grid, amplitude_envelope, label='Hilbert envelope', linestyle='--', color='r')
    ax0.set_xlabel("$t\ (\\textrm{s})$", size='15')
    ax0.set_ylabel("Amplitude", size='15')
    ax0.legend()
    ax0.set_xlim([0, 1])
    ax0.tick_params(axis='both', which='major', labelsize=15)

    ax1.plot(t_grid[1:], freq_real, label='Real frequency', color='k')
    ax1.plot(t_grid[1:], instantaneous_frequency, label='Hilbert frequency', linestyle='--', color='r')
    ax1.set_xlabel("$t\ (\\textrm{s})$", size='15')
    ax1.set_xlim([0, 1])
    ax1.set_ylabel("Instantaneous Frequency", size='15')
    ax1.tick_params(axis='both', which='major', labelsize=15)
    ax1.legend()

    fig.tight_layout()
    plt.savefig('hilbert_example.png', dpi=300)
    plt.close()