import numpy as np



def well_boundary_condition(X, Y, p, q, coef, N_x, N_y, r_w):
    for i in range(N_x):
        for j in range(N_y):
            r = np.sqrt((X[i]) ** 2 + (Y[j]) ** 2)
            if r <= r_w:
                p[i, j] += q * coef * r_w * r_w / 2
    return p


def solve_for_one_well_explicit(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, eta):
    pressure_w = []
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]
    dt = 1 / (2 * eta * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2  # шаг по времени в сутках c учетом устойчивости
    if 5 < dt < T: dt = T // (50 * 12)
    time = []
    a, b = np.where(X == 0), np.where(Y == 0)
    period = np.linspace(int(dt), T + int(dt), int(T / dt) + 1)
    for t in period:
        time.append(t)
        p_new = pressure_start.copy()
        for i in range(1, N_x - 1):
            for j in range(1, N_y - 1):
                p_new[i, j] = pressure_start[i, j] + eta * dt * (
                        (pressure_start[i + 1, j] - 2 * pressure_start[i, j] + pressure_start[i - 1, j]) / dx ** 2 +
                        (pressure_start[i, j + 1] - 2 * pressure_start[i, j] + pressure_start[i, j - 1]) / dy ** 2
                )
        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)
        pressure_w.append(pressure_start[int(a[0]), int(b[0])])

    return pressure_start, pressure_w, time


