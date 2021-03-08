import argparse
import numpy as np
import time
from utils.read_input_file import p_air, dens_air, h_ratio
from utils.read_input_file import read_input_value, init_input_data
from calc_pressure import call_calc_state
from calc_energy import calc_energy
from utils.calc_coefficient import incomp_condensation_coef, incomp_force_coef
from calc_flow import calc_flow_and_mass_flow
from utils.output import output_to_csv
from utils.curve_fit import exec_curve_fit


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('load_file_name', help='format: example.yml')
    parser.add_argument('save_file_name', help='format: amplitude_period.csv')
    args = parser.parse_args()
    return args


def main(args):
    total_time_start = time.time()

    load_file_name = args.load_file_name
    save_file_name = args.save_file_name
    load_file_path = 'inputs/' + load_file_name
    save_file_path = 'outputs/' + save_file_name

    print('#####################################################')
    print(f"loading input file {load_file_name}")
    print('#####################################################')

    input_data = read_input_value(load_file_path)

    print('#####################################################')
    print('initialize input data')
    print('#####################################################')

    period, n, total_time, n_diam, D0, Zd, Zd0, phase_diff, p0, p0_delta, d_ratio, A, A0 = init_input_data(
        input_data)

    print('#####################################################')
    print("start calculate pressure")
    print('#####################################################')
    start_time = time.time()

    t_list, p_list, v0_list, dv0dt_list, p_delta_list = call_calc_state(
        n, period, total_time, phase_diff, d_ratio, A0, A, Zd, Zd0, p0, p0_delta)

    end_time = time.time()
    p_calc_time = divmod(end_time-start_time, 60)
    print('#####################################################')
    print(f'calculation time: {int(p_calc_time[0])}m {int(p_calc_time[1])}s')
    print("calculate pressure finished")
    print('#####################################################')

    p_diff_list = p_list - p_air
    p_correct_diff_list = p_delta_list + p_diff_list

    tip_point = 0
    end_point = 0
    for i in range(len(v0_list) - 1):
        prev = v0_list[i-1]
        current = v0_list[i]
        if ((current < A0 * Zd0) and (A0 * Zd0 < prev)):
            if (tip_point == 0):
                tip_point = i-1
            end_point = i

    guess_pres = exec_curve_fit(
        period, t_list[tip_point:end_point], p_correct_diff_list[tip_point:end_point])
    print('pressure')
    print('freq, amplitude, phase, offset')
    print(guess_pres)

    c_ci = incomp_condensation_coef(d_ratio)
    f_i = incomp_force_coef(c_ci)

    flow_list, mass_flow_list, dens_list = calc_flow_and_mass_flow(
        f_i, p_list, A)
    guess_flow = exec_curve_fit(
        period, t_list[tip_point:end_point], flow_list[tip_point:end_point])
    guess_mass_flow = exec_curve_fit(
        period, t_list[tip_point:end_point], mass_flow_list[tip_point:end_point])

    print('flow')
    print('freq, amplitude, phase, offset')
    print(guess_flow)

    print('mass flow')
    print('freq, amplitude, phase, offset')
    print(guess_mass_flow)

    v0_list = np.array(v0_list)
    zd_list = v0_list / A0

    dv0dt_list = np.array(dv0dt_list)
    dzddt_list = dv0dt_list / A0
    dzdt_list = (-1) * dzddt_list

    # wave_energy_per_period = calc_energy(period, A0, tip_point, end_point, t_list, p_correct_diff_list, dzdt_list)

    phase_diff = (guess_pres[2] - np.pi) if (guess_pres[1] >= 0) else ((guess_pres[2] + np.pi) - np.pi)
    wave_energy_per_period_2 = (1/2) * guess_pres[1] * Zd * A0 * (2 * np.pi / period) * np.sin(phase_diff)
    print('wave energy per period')
    # print(wave_energy_per_period)
    print('press amp, phase')
    print(guess_pres[1], guess_pres[2])
    print(wave_energy_per_period_2)

    print('#####################################################')
    print('file outputing')
    print('#####################################################')
    output_to_csv(t_list, p_diff_list, p_correct_diff_list, flow_list,
                  mass_flow_list, zd_list, dens_list, save_file_path)

    total_time_end = time.time()
    total_time = divmod(total_time_end-total_time_start, 60)

    print('#####################################################')
    print(f'output result {save_file_name}')
    print(f'total time: {int(total_time[0])}m {int(total_time[1])}s')
    print('#####################################################')


if __name__ == '__main__':
    args = get_arg()
    main(args)
