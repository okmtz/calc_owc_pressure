


def calc_energy(period, area: 'area on water line', tip_point, end_point, t_list: 'time list', p_list: 'pressure list', dzdt_list: 'water line diff'):
    n = len(t_list)
    dx = (end_point - tip_point) / n
    energy_per_time_list = p_list * dzdt_list * area
    energy_per_time_list_correct = [(i if (i >= 0) else ((-1) * i)) for i in energy_per_time_list]
    energy_sum = 0
    for i in range(0, n, 1):
        x1 = tip_point + dx * i
        x2 = tip_point + dx * (i+1)
        f1 = energy_per_time_list_correct[i-1]
        f2 = energy_per_time_list_correct[i]
        energy_sum = energy_sum + (f1 + f2) * dx / 2
    
    period_times = (end_point - tip_point) / period
    energy_per_period = energy_sum / period_times

    return energy_per_period