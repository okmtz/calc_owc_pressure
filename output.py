import pandas as pd
import numpy as np


def output_to_csv(t_list, p_diff_list, p_correct_diff_list, v0_list, save_file_name):
    t_p_list = pd.DataFrame(
        {'t': t_list, 'p': p_diff_list, 'p_corrected': p_correct_diff_list, 'v0_list': v0_list}, index=None)
    try:
        t_p_list.to_csv(save_file_name)
    except Exception as e:
        print(e)

    print(f"calc pressure output to {save_file_name}")
