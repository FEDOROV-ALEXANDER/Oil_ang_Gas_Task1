import numpy as np
from scipy.sparse import diags, csc_matrix, kron
from scipy.sparse.linalg import spsolve
import time as tm


def well_boundary_condition(X, Y, p, q, coef, N_x, N_y, r_w):
    for i in range(N_x):
        for j in range(N_y):
            r = np.sqrt((X[i]) ** 2 + (Y[j]) ** 2)
            if r <= r_w:
                p[i, j] += 13.76
                # print(p[i, j])# q * coef * r_w
    return p


def solve_for_one_well_implicit(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, eta):
    begin = tm.time()
    pressure_w = []
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]
    dt = 1  # шаг по времени в сутках
    time = []
    a, b = np.where(X == 0), np.where(Y == 0)

    # Коэффициенты для системы уравнений
    alpha = eta * dt / (dx ** 2)
    beta = eta * dt / (dy ** 2)

    for t in range(1, T + 1, dt):
        time.append(t)

        # Создание матрицы и вектора правой части
        A = diags([-alpha, 1 + 2 * alpha + 2 * beta, -alpha], [-1, 0, 1], shape=(N_x, N_x)).tocsc()
        B = diags([-beta, 1 + 2 * alpha + 2 * beta, -beta], [-1, 0, 1], shape=(N_y, N_y)).tocsc()
        M = kron(B, csc_matrix(np.eye(N_x))) + kron(csc_matrix(np.eye(N_y)), A)
        b = pressure_start.flatten()

        # Решение системы уравнений
        p_new = spsolve(M, b)
        pressure_start = p_new.reshape((N_x, N_y))

        # Граничное условие на скважине
        pressure_start = well_boundary_condition(X, Y, pressure_start, q, coef, N_x, N_y, r_w)
        pressure_w.append(pressure_start[int(a[0]), int(b[0])])
        print(t, tm.time() - begin)
    return pressure_start, pressure_w, time


def solve_for_one_well_explicit(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, eta):
    pressure_w = []
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = X.shape[0], Y.shape[0]
    dt = 1 / (2 * eta * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2  # шаг по времени в сутках c учетом устойчивости
    if dt > 5: dt = 5
    time = []
    a, b = np.where(X == 0), np.where(Y == 0)

    for t in range(1, T + 1, dt):
        time.append(t)

        p_new = pressure_start.copy()
        for i in range(1, N_x - 1):
            for j in range(1, N_y - 1):
                p_new[i, j] = pressure_start[i, j] + eta * dt * (
                        (pressure_start[i + 1, j] - 2 * pressure_start[i, j] + pressure_start[i - 1, j]) / dx ** 2 +
                        (pressure_start[i, j + 1] - 2 * pressure_start[i, j] + pressure_start[i, j - 1]) / dy ** 2
                )
        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)
        print(p_new[int(a[0]), int(b[0])], int(a[0]), int(b[0]), pressure_start[int(a[0]), int(b[0])])
        pressure_w.append(pressure_start[int(a[0]), int(b[0])])

    return pressure_start, pressure_w, time
