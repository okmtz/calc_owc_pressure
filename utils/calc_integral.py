def calc_integral(x_length, x_tip, x_end, y_list):
    dx = (x_end - x_tip) / x_length
    integral_val = 0
    for i in range(0, x_length, 1):
        x1 = x_tip + dx * i
        x2 = x_tip + dx * (i+1)
        f1 = y_list[i-1]
        f2 = y_list[i]
        integral_val += (f1 + f2) * dx / 2

    return integral_val
