from utils.read_input_file import p_air, dens_air, h_ratio


def calc_density(p) -> '断熱仮定での密度':
    dens = dens_air * ((p / p_air) ** (1/h_ratio))
    return dens
