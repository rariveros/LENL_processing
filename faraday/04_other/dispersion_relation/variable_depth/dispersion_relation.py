from back_process import *

if __name__ == "__main__":
    wave_length = np.arange(3, 10, 0.02)
    g = 9.81
    depth_01 = 2
    depth_02 = 1.5
    depth_03 = 1
    depth_04 = 0.5
    omega_01 = np.sqrt((2 * np.pi * g / wave_length) * np.tanh(2 * np.pi * depth_01 / wave_length))
    omega_02 = np.sqrt((2 * np.pi * g / wave_length) * np.tanh(2 * np.pi * depth_02 / wave_length))
    omega_03 = np.sqrt((2 * np.pi * g / wave_length) * np.tanh(2 * np.pi * depth_03 / wave_length))
    omega_04 = np.sqrt((2 * np.pi * g / wave_length) * np.tanh(2 * np.pi * depth_04 / wave_length))
    plt.plot(wave_length, omega_01 / (2 * np.pi), label='$h_0 = $' + str(depth_01) + ' cm')
    plt.plot(wave_length, omega_02 / (2 * np.pi), label='$h_0 = $' + str(depth_02) + ' cm')
    plt.plot(wave_length, omega_03 / (2 * np.pi), label='$h_0 = $' + str(depth_03) + ' cm')
    plt.plot(wave_length, omega_04 / (2 * np.pi), label='$h_0 = $' + str(depth_04) + ' cm')
    plt.grid()
    plt.xlim(wave_length[0], wave_length[-1])
    plt.ylabel('Frequency ($f_{w}$)')
    plt.xlabel('Wavelength ($\lambda$)')
    plt.legend()
    plt.show()