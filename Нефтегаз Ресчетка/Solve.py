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
    a = [X[0], X[1], Y[0], Y[1]]
    print(a)
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    N_x, N_y = len(X), len(Y)
    dt = 1 / (2 * eta * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2  # шаг по времени в сутках c учетом устойчивости
    if 5 < dt < T: dt = T // (50 * 12)
    time = []
    a, b = np.where(X == 0), np.where(Y == 0)
    period = np.arange(dt, T + dt, dt)

    # Векторизация вычислений
    pressure_start = pressure_start.astype(np.float64)
    p_new = np.empty_like(pressure_start)
    laplacian = np.zeros_like(pressure_start)

    for t in period:
        time.append(t)

        # Вычисление лапласиана
        laplacian[1:-1, 1:-1] = (pressure_start[2:, 1:-1] - 2 * pressure_start[1:-1, 1:-1] + pressure_start[:-2,
                                                                                             1:-1]) / dx ** 2 + \
                                (pressure_start[1:-1, 2:] - 2 * pressure_start[1:-1, 1:-1] + pressure_start[1:-1,
                                                                                             :-2]) / dy ** 2

        # Обновление давления
        p_new[1:-1, 1:-1] = pressure_start[1:-1, 1:-1] + eta * dt * laplacian[1:-1, 1:-1]

        # Применение граничных условий
        pressure_start = well_boundary_condition(X, Y, p_new, q, coef, N_x, N_y, r_w)

        # Сохранение давления на скважине
        pressure_w.append(pressure_start[int(a[0]), int(b[0])])

    return pressure_start, pressure_w, time



