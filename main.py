import argparse
import numpy as np
import time
from read_input_file import p_air, dens_air, h_ratio
from read_input_file import read_input_value, init_input_data
from calc_pressure import call_calc_state
from output import output_to_csv


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
    print(f"loading input file {args.load_file_name}")
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

    print('#####################################################')
    print('file outputing')
    print('#####################################################')
    output_to_csv(t_list, p_diff_list, p_correct_diff_list, save_file_path)

    total_time_end = time.time()
    total_time = divmod(total_time_end-total_time_start, 60)
    print('#####################################################')
    print(f'output result {save_file_name}')
    print(f'total time: {int(total_time[0])}m {int(total_time[1])}s')
    print('#####################################################')


if __name__ == '__main__':
    args = get_arg()
    main(args)