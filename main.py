import os
import sys
import argparse
import numpy as np
import pandas as pd
from read_input_file import read_input_value

def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('load_file_path', help='require', type='str')
    args = parser.parse_args()
    return args

def init_input_data(input_data):
    period = input_data['input']['period']
    n = input_data['input']['n']
    total_time = input_data['input']['total_time']
    n_diam = input_data['input']['n_diam']
    D0 = input_data['input']['D0']
    h_ratio = input_data['input']['h_ratio']
    p_air = input_data['input']['p_air']
    dens_air = input_data['input']['dens_air']
    Zh = input_data['input']['Zh']
    Zh0 = input_data['input']['Zh0']
    phase_diff = input_data['input']['phase_diff']
    # 絞り直径比
    d_ratio = n_diam / D0
    # カラム内断面積
    A = ((D0 / 2) ** 2) ** np.pi
    A0 = A * (d_ratio ** 2)
    return period, n, total_time, n_diam, D0, h_ratio, p_air, dens_air,Zh, Zh0, phase_diff, d_ratio, A, A0

def main(args):
    load_file_path = args.load_file_path
    input_data = read_input_value(load_file_path)
    period, n, total_time, n_diam, D0, h_ratio, p_air, dens_air,Zh, Zh0, phase_diff, d_ratio, A, A0 = init_input_data(input_data)
    t_list, p_list, v0_list, p_delta_list = call_calc_state(n, period, total_time, phase_diff, d_ratio, A0, A, Zh, Zh0)
    p_list_diff = p_list - p_air
    p_list_correct = p_delta_list + p_list
    output_to_csv(save_path)

if __name__ == '__main__':
    args = get_arg()
    main(args)