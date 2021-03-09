import numpy as np
from utils.read_input_file import p_air, dens_air, h_ratio
from utils.calc_coefficient import incomp_condensation_coef, incomp_force_coef, comp_condensation_coef
from calc_flow import forward_flow, back_flow
from utils.calc_density import calc_density


def call_calc_state(n, period, total_time, phase_diff, d_ratio, A0, A, Zd, Zd0, p0, p0_delta) -> '圧力, 圧力勾配, 空気室内容積変位計算の呼び出し':
    h = period / n  # 分割時間
    t = np.arange(0, total_time, h)
    c_freq = 2 * np.pi / period  # 円振動数
    total_split = len(t)
    p, V0, dV0dt, dV02dt2, p_delta = [np.empty(total_split) for i in range(5)]
    p[0], p_delta[0] = p_air + p0, p0_delta
    V0[0], dV0dt[0], dV02dt2[0] = (Zd0 + Zd * np.sin(phase_diff)) * A0, (c_freq * Zd * np.cos(
        phase_diff)) * A0, ((-1) * ((c_freq) ** 2) * Zd * np.sin(phase_diff)) * A0
    t, p, V0, dV0dt, p_delta = runge_kutta(
        h, t, total_split, c_freq, phase_diff, p, p_delta, V0, dV0dt, dV02dt2, d_ratio, A0, A, Zd, Zd0)

    return t, p, V0, dV0dt, p_delta


def runge_kutta(h: '時間分割', t, total_split, c_freq, phase_diff, p, p_delta, V0, dV0dt, dV02dt2, d_ratio, A0, A, Zd, Zd0) -> 'Runge-Kutta法を用いた圧力の計算, 圧力勾配, 空気室内容積変位の計算':
    # 非圧縮性の縮流係数
    c_ci = incomp_condensation_coef(d_ratio)
    # 非圧縮性の力欠損係数
    f_i = incomp_force_coef(c_ci)

    # 方程式を解くための反復計算
    for i in range(total_split - 1):
        #######runge-kutta法により圧力を計算#######
        arg_list = [c_freq, d_ratio, V0[i], dV0dt[i], A, f_i]  # dpdtの引数
        k_1 = h * calc_dpdt(p[i], t[i], *arg_list)
        k_2 = h * calc_dpdt(p[i] + k_1 / 2, t[i] + h/2, *arg_list)
        k_3 = h * calc_dpdt(p[i] + k_2 / 2, t[i] + h/2, *arg_list)
        k_4 = h * calc_dpdt(p[i] + k_3, t[i] + h, *arg_list)
        p[i+1] = p[i] + 1/6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        #####################################

        ###########空気室内容積を計算############
        ###############中型模型################
        V0[i+1] = (Zd0 + Zd * np.sin(c_freq * t[i] + phase_diff)) * A0
        dV0dt[i+1] = (c_freq * Zd *
                      np.cos(c_freq * t[i] + phase_diff)) * A0
        dV02dt2[i+1] = ((-1) * ((c_freq) ** 2) * Zd *
                        np.sin(c_freq * t[i] + phase_diff)) * A0
        #####################################

        ##########圧力勾配を計算################
        dens_prev = calc_density(p[i])
        dens_current = calc_density(p[i+1])

        arg_list_2 = [p[i], p[i+1], f_i, h, dens_prev, dens_current,
                      V0[i+1], dV0dt[i+1], dV02dt2[i+1], A, A0]  # calc_p_deltaの引数
        p_delta[i+1] = calc_forward_p_delta(*arg_list_2) if (
            p[i+1] > p_air) else calc_back_p_delta(*arg_list_2)
        #####################################

        # pがnanの場合はbreakさせる
        if (np.isnan(p[i+1])):
            raise Exception('pressure is not nan')

    return t, p, V0, dV0dt, p_delta


def calc_dpdt(p, t, c_freq, d_ratio, V0, dV0dt, A, f_ci) -> '圧力変動':
    dens = calc_density(p)
    if (p > p_air):
        # 押出過程
        c_c = comp_condensation_coef(f_ci, p, p_air)
        flow = forward_flow(c_c, A, p, dens)
        dpdt = (-7/5) * p * ((dV0dt / V0) + ((dens_air / dens) * (flow / V0)))
    else:
        # 吸込過程
        c_c = comp_condensation_coef(f_ci, p_air, p)
        flow = back_flow(c_c, A, p)
        dpdt = (-7/5) * p * ((dV0dt / V0) +
                             (((dens_air / dens) ** h_ratio) * (((-1) * flow) / V0)))
    return dpdt


def calc_forward_p_delta(p_prev, p_current, f_ci, h, dens_prev, dens_current, V0, dV0dt, dV02dt2, A, A0) -> '押出過程での圧力勾配を計算':
    ########## i番目の流量を求める #############
    if (p_prev > p_air):
        # 押出過程
        c_c_prev = comp_condensation_coef(f_ci, p_prev, p_air)
        flow_prev = forward_flow(c_c_prev, A, p_prev, dens_prev)
    else:
        # 吸込過程
        c_c_prev = comp_condensation_coef(f_ci, p_air, p_prev)
        flow_prev = (-1) * back_flow(c_c_prev, A, p_prev)
    ######################################

    ########## i+1番目の流量を求める###########
    c_c_current = comp_condensation_coef(f_ci, p_current, p_air)
    flow_current = forward_flow(c_c_current, A, p_current, dens_current)
    ######################################

    p_delta = forward_delta_p(dens_current, V0, dV0dt,
                              dV02dt2, flow_prev, flow_current, h, A0)
    return p_delta


def calc_back_p_delta(p_prev, p_current, f_ci, h, dens_prev, dens_current, V0, dV0dt, dV02dt2, A, A0) -> '吸込過程での圧力勾配を計算':
    ########## i番目の流量を求める #############
    if (p_prev > p_air):
        # 押出過程
        c_c_prev = comp_condensation_coef(f_ci, p_prev, p_air)
        flow_prev = forward_flow(c_c_prev, A, p_prev, dens_prev)
    else:
        # 吸込過程
        c_c_prev = comp_condensation_coef(f_ci, p_air, p_prev)
        flow_prev = (-1) * back_flow(c_c_prev, A, p_prev)
    ######################################

    ########## i+1番目の流量を求める###########
    c_c_current = comp_condensation_coef(f_ci, p_air, p_current)
    flow_current = (-1) * back_flow(c_c_current, A, p_current)
    ######################################

    p_delta = back_delta_p(dens_current, V0, dV0dt,
                           dV02dt2, flow_prev, flow_current, h, A0)
    return p_delta


def forward_delta_p(dens, V0, dV0dt, dV02dt2, flow_prev, flow_current, delta_t, A0) -> '押出圧力補正':
    flow_diff = (flow_current - flow_prev) / delta_t  # 流量変動
    delta_p = (-1) * ((dens ** 2) / (A0 ** 2)) * (V0 * (dV02dt2 + (dens_air / dens) *
                                                        flow_diff) + (1 / 2) * (dV0dt + (1 / dens) * (dens_air * flow_current)) * dV0dt)  # 中型模型
    return delta_p


def back_delta_p(dens, V0, dV0dt, dV02dt2, flow_prev, flow_current, delta_t, A0) -> '吸込圧力補正':
    flow_diff = (flow_current - flow_prev) / delta_t  # 流量変動
    delta_p = (-1) * ((dens ** 2) / (A0 ** 2)) * (V0 * (dV02dt2 + ((7/2) * ((dens_air / dens) ** h_ratio) * (flow_diff)) - ((5/2) * (dens_air / dens) *
                                                                                                                            (flow_diff))) + (1/2) * (dV0dt + ((1 / 2) * ((7 * ((dens_air / dens) ** (h_ratio + 1))) - 5) * (1 / dens) * (dens_air * flow_current))) * dV0dt)  # 中型模型
    return delta_p
