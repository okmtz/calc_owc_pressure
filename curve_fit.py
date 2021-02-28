import numpy as np
from scipy.optimize import curve_fit


def init(data_list, freq):
    guess_freq = freq
    guess_amplitude = 3*np.std(data_list)/(2**0.5)
    guess_phase = 0
    guess_offset = np.mean(data_list)

    p0 = [guess_freq, guess_amplitude,
          guess_phase, guess_offset]

    return p0


def my_sin(t, freq, amp, phase, offset):
    return np.sin(t * freq + phase) * amp + offset


def exec_curve_fit(period, t_list, data_list):
    freq = 2 * np.pi / period
    p0 = init(data_list, freq)
    # now do the fit
    fit = curve_fit(my_sin, t_list, data_list, p0=p0)
    # we'll use this to plot our first estimate. This might already be good enough for you
    data_first_guess = my_sin(t_list, *p0)
    # recreate the fitted curve using the optimized parameters
    data_fit = my_sin(t_list, *fit[0])
    return fit[0]
