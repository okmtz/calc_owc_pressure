


def calc_wave_energy(period, area: 'area on water line', t_list, p_list: 'pressure list', dzdt_list: 'water line diff')-> '水面が空気室に対してなす仕事':
    n = len(t_list)
    t_tip = t_list[0]
    t_end = t_list[-1]
    dx = (t_end - t_tip) / n
    energy_per_time_list = p_list * dzdt_list * area

    energy_sum = 0
    for i in range(0, n, 1):
        x1 = t_tip + dx * i
        x2 = t_tip + dx * (i+1)
        f1 = energy_per_time_list[i-1]
        f2 = energy_per_time_list[i]
        energy_sum = energy_sum + (f1 + f2) * dx / 2
    
    period_times = (t_end - t_tip) / period
    energy_per_period = energy_sum / period_times

    return energy_per_period
