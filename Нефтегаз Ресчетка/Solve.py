import numpy as np
import matplotlib.pyplot as plt

def well_boundary_condition(X, Y, p, q, coef, N_x, N_y, r_w):
    for i in range(N_x):
        for j in range(N_y):
            r = np.sqrt((X[i]) ** 2 + (Y[j]) ** 2)
            if r <= r_w:
                p[i, j] +=  10 #q * coef * r_w
    return p

def solve_for_one_well(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, dt, eta):
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]

    for t in range(1, int(T / dt) + 1):
        p_new = pressure_start.copy()
        for i in range(1, N_x - 1):
            for j in range(1, N_y - 1):
                p_new[i, j] = pressure_start[i, j] + eta * dt * (
                        (pressure_start[i + 1, j] - 2 * pressure_start[i, j] + pressure_start[i - 1, j]) / dx ** 2 +
                        (pressure_start[i, j + 1] - 2 * pressure_start[i, j] + pressure_start[i, j - 1]) / dy ** 2
                )
        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)

    # Найдем давление в точке скважины
    well_index_x = np.argmin(np.abs(X))
    well_index_y = np.argmin(np.abs(Y))
    pressure_w = pressure_start[well_index_x, well_index_y]

    return pressure_start, pressure_w