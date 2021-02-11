import argparse
import numpy as np
import time
from read_input_file import p_air, dens_air, h_ratio
from read_input_file import read_input_value, init_input_data
from calc_pressure import call_calc_state
from calc_coefficient import incomp_condensation_coef, incomp_force_coef
from calc_flow import calc_flow_and_mass_flow
from output import output_to_csv
from curve_fit import exec_curve_fit


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

    period, n, total_time, n_diam, D0, Zh, Zh0, phase_diff, p0, p0_delta, d_ratio, A, A0 = init_input_data(input_data)

    print('#####################################################')
    print("start calculate pressure")
    print('#####################################################')
    start_time = time.time()

    t_list, p_list, v0_list, p_delta_list = call_calc_state(
        n, period, total_time, phase_diff, d_ratio, A0, A, Zh, Zh0, p0, p0_delta)

    end_time = time.time()
    p_calc_time = divmod(end_time-start_time, 60)
    print('#####################################################')
    print(f'calculation time: {int(p_calc_time[0])}m {int(p_calc_time[1])}s')
    print("calculate pressure finished")
    print('#####################################################')
    
    p_diff_list = p_list - p_air
    p_correct_diff_list = p_delta_list + p_diff_list

    zero_pos = 0
    for i in range(len(v0_list)-1):
        prev = v0_list[i-1]
        current = v0_list[i]
        if ((current < A0*Zh0) and (A0*Zh0 < prev)):
            print(prev, current)
            print(i)
            zero_pos = i-1
            break

    print(zero_pos)
    guess_pres = exec_curve_fit(period, t_list[zero_pos:], p_correct_diff_list[zero_pos:])
    print('pressure')
    print('freq, apm, phase, offset')
    print(guess_pres)

    c_ci = incomp_condensation_coef(d_ratio)
    # 非圧縮性の力欠損係数
    f_i = incomp_force_coef(c_ci)
    flow_list, mass_flow_list = calc_flow_and_mass_flow(f_i, p_list, A)
    guess_flow = exec_curve_fit(period, t_list[zero_pos:], flow_list[zero_pos:])
    guess_mass_flow = exec_curve_fit(period, t_list[zero_pos:], mass_flow_list[zero_pos:])
    print('flow')
    print('freq, apm, phase, offset')
    print(guess_flow)

    print('mass flow')
    print('freq, apm, phase, offset')
    print(guess_mass_flow)

    # print('#####################################################')
    # print('file outputing')
    # print('#####################################################')
    v0_list = np.array(v0_list)
    output_to_csv(t_list[zero_pos:], p_diff_list[zero_pos:], p_correct_diff_list[zero_pos:], v0_list[zero_pos:], save_file_path)

    # # total_time_end = time.time()
    # # total_time = divmod(total_time_end-total_time_start, 60)
    # print('#####################################################')
    # # print(f'output result {save_file_name}')
    # # print(f'total time: {int(total_time[0])}m {int(total_time[1])}s')
    # print('#####################################################')


if __name__ == '__main__':
    args = get_arg()
    main(args)
