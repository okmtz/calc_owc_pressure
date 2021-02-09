import pandas as pd


def output_to_csv(t_list, p_diff_list, p_correct_diff_list, flow_list, mass_flow_list, dens_list, zd_list, save_file_name):
    t_result_list = pd.DataFrame(
        {'t': t_list, 'p': p_diff_list, 'p_corrected': p_correct_diff_list, 'flow': flow_list, 'mass_flow': mass_flow_list, 'dens': dens_list, 'zd_list': zd_list}, index=None)
    try:
        t_result_list.to_csv(save_file_name)
    except Exception as e:
        print(e)

    print(f"calc pressure output to {save_file_name}")
