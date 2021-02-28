from utils.read_input_file import p_air, dens_air, h_ratio


def incomp_force_coef(c_ci) -> '非圧縮性力欠損係数':
    return ((1 / c_ci) - (1 / (2 * (c_ci ** 2))))


def incomp_condensation_coef(d_ratio) -> '非圧縮性の縮流係数':
    # 流量係数
    flow_coef = 0.598 - 0.003 * (d_ratio ** 2) + 0.404 * (d_ratio ** 4)
    return (flow_coef / ((1 + (d_ratio ** 4) * (flow_coef ** 2)) ** (1/2)))


def comp_condensation_coef(f_ci_c, p_up, p_down) -> '縮流係数':
    p_ratio = p_up / p_down
    h_ratio_rev = 1 / h_ratio
    return ((1 / (2 * f_ci_c)) * (p_ratio ** h_ratio_rev) * (1 - (1 - ((2 * f_ci_c * (1 - h_ratio_rev)) * (1 - (1 / p_ratio)) / (1 - (p_ratio) ** (h_ratio_rev - 1)))) ** (1/2)))
