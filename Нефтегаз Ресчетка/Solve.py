import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve


def well_boundary_condition(X, Y, p, q, coef, N_x, N_y, r_w):
    for i in range(N_x):
        for j in range(N_y):
            r = np.sqrt((X[i]) ** 2 + (Y[j]) ** 2)
            if r <= r_w:
                p[i, j] += q * coef[i, j] * r_w * r_w / 2
    return p

#Явный метод
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
    dt = 1 / (3 * eta.max() * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2  # шаг по времени в сутках c учетом устойчивости

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
        productivity.append(q / pressure_start[int(a[0]), int(b[0])] * 10000)
        history.append(pressure_start / 10000)
    return pressure_start / 10000, pressure_w, productivity, time, history

# продольно поперечные прогонки

def solve_for_one_well_crank_nicolson(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, eta):
    pressure_w = []
    productivity = []
    history = []
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]
    dt = 1  / (3 * eta.max() * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2
    time = np.arange(0, T + dt, dt)

    a, b = np.where(X == 0), np.where(Y == 0)

    for t in time:
        p_new = pressure_start.copy()

        # Метод Кранка-Николсона
        for i in range(1, N_x-1):
            for j in range(1, N_y-1):
                p_new[i, j] = pressure_start[i, j] + 0.5 * eta[i, j] * dt * (
                    (pressure_start[i+1, j] - 2 * pressure_start[i, j] + pressure_start[i-1, j]) / dx**2 +
                    (pressure_start[i, j+1] - 2 * pressure_start[i, j] + pressure_start[i, j-1]) / dy**2 +
                    (p_new[i+1, j] - 2 * p_new[i, j] + p_new[i-1, j]) / dx**2 +
                    (p_new[i, j+1] - 2 * p_new[i, j] + p_new[i, j-1]) / dy**2
                )

        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)
        pressure_w.append(pressure_start[int(a[0]), int(b[0])] / 10000)
        productivity.append(q / pressure_start[int(a[0]), int(b[0])] * 10000)
        history.append(pressure_start / 10000)
    return pressure_start / 10000, pressure_w, productivity, time, history