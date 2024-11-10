import numpy as np


def well_boundary_condition(X, Y, p, q, coef, N_x, N_y, r_w):
    for i in range(N_x):
        for j in range(N_y):
            r = np.sqrt((X[i]) ** 2 + (Y[j]) ** 2)
            if r <= r_w:
                p[i, j] += q * coef[i, j] * r_w * r_w / 2
    return p


def solve_for_one_well_explicit(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, eta):
    pressure_w = []
    productivity = []
    history = []
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]

    # Вычисление максимального шага по времени с учетом устойчивости
    dt = 1 / (4 * eta.mean() * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2  # шаг по времени в сутках c учетом устойчивости
    if 20 < dt < T: dt = T // (30 * 12)
    # if dt < 1: dt = 1

    time = np.arange(dt, T + dt, dt)

    a, b = np.where(X == 0), np.where(Y == 0)

    for t in time:
        p_new = pressure_start.copy()
        p_new[1:-1, 1:-1] = pressure_start[1:-1, 1:-1] + eta[1:-1, 1:-1] * dt * (
                (pressure_start[2:, 1:-1] - 2 * pressure_start[1:-1, 1:-1] + pressure_start[:-2, 1:-1]) / dx ** 2 +
                (pressure_start[1:-1, 2:] - 2 * pressure_start[1:-1, 1:-1] + pressure_start[1:-1, :-2]) / dy ** 2
        )

        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)
        pressure_w.append(pressure_start[int(a[0]), int(b[0])] / 10000)
        # Посчитаю продуктивность, руководствовался этим: https://ru.wikipedia.org/wiki/Продуктивность_(нефтедобыча),
        # https: // vseonefti.ru / useful /
        productivity.append(q / -pressure_start[int(a[0]), int(b[0])] * 10000)
        history.append(pressure_start / 10000)
    return pressure_start / 10000, pressure_w, productivity, time, history
