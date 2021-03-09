from utils.calc_integral import calc_integral
import numpy as np


def calc_wave_energy(period, A0: 'area on water line', t_list, p_list: 'pressure list', dzdt_list: 'water line diff')-> '水面が空気室に対してなす仕事':
    n = len(t_list)
    t_tip = t_list[0]
    t_end = t_list[-1]
    energy_per_time_list = p_list * dzdt_list * A0
    energy_sum = calc_integral(n, t_tip, t_end, energy_per_time_list)
    period_times = (t_end - t_tip) / period
    wave_energy_per_period = energy_sum / period_times

    return wave_energy_per_period


def calc_air_kinetic_energy(period, A, t_list, flow_list, mass_flow_list)-> '空気の運動エネルギー':
    air_velocity_list = flow_list / A
    n = len(t_list)
    t_tip = t_list[0]
    t_end = t_list[-1]
    energy_per_time_list = (1 / 2) * mass_flow_list * (air_velocity_list ** 2)
    energy_per_time_list = np.abs(energy_per_time_list)
    energy_sum = calc_integral(n, t_tip, t_end, energy_per_time_list)
    period_times = (t_end - t_tip) / period
    air_kinetic_energy_per_period = energy_sum / period_times

    return air_kinetic_energy_per_period