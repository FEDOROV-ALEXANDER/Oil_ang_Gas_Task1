import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags, linalg

def solve_for_one_well_implicit(X, Y, x_w, y_w, q, r_w, coef, pressure_start, T, dt, eta):
    X = X - x_w
    Y = Y - y_w
    dx = X[1] - X[0]
    dy = Y[1] - Y[0]
    Nx, Ny = len(X), len(Y)

    # Коэффициенты для матрицы
    alpha_x = eta * dt / dx**2
    alpha_y = eta * dt / dy**2

    # Создание матрицы для системы уравнений
    main_diag = np.ones((Nx, Ny)) * (1 + 2 * alpha_x + 2 * alpha_y)
    off_diag_x = np.ones((Nx, Ny)) * -alpha_x
    off_diag_y = np.ones((Nx, Ny)) * -alpha_y

    # Граничные условия
    main_diag[0, :] = 1
    main_diag[-1, :] = 1
    main_diag[:, 0] = 1
    main_diag[:, -1] = 1

    off_diag_x[0, :] = 0
    off_diag_x[-1, :] = 0
    off_diag_y[:, 0] = 0
    off_diag_y[:, -1] = 0

    # Формирование матрицы
    diagonals = [main_diag.flatten(), off_diag_x[:-1, :].flatten(), off_diag_x[1:, :].flatten(),
                 off_diag_y[:, :-1].flatten(), off_diag_y[:, 1:].flatten()]
    A = diags(diagonals, [0, -Nx, Nx, -1, 1]).toarray()

    # Решение системы уравнений на каждом временном шаге
    for t in range(1, int(T / dt) + 1):
        b = pressure_start.flatten()

        # Применение граничных условий на внутренней границе (скважина)
        for i in range(Nx):
            for j in range(Ny):
                r = np.sqrt((X[i])**2 + (Y[j])**2)
                if r <= r_w:
                    b[i * Ny + j] = q * coef * r

        # Решение системы уравнений
        p_new = linalg.spsolve(A, b).reshape((Nx, Ny))
        pressure_start = p_new

    # Найдем давление в точке скважины
    well_index_x = np.argmin(np.abs(X))
    well_index_y = np.argmin(np.abs(Y))
    pressure_w = pressure_start[well_index_x, well_index_y]

    return pressure_start, pressure_w

# Параметры задачи
length, width = 15000, 15000  # [м] геометрические размеры рассчитываемой области
dx, dy = 100, 100  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1 # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 365

# координаты скважины
x_w = 3000
y_w = 3000
r_w = 1.5
# пока будет одна скважина, нагнетательная
q_injection = 10  # [м3/сут] дебит нагнетательных скважин

B = 5  # Объемный коэффициент
h = 20  # толщина пласта

# параметры взяты плюс-минус от балды
viscosity = 1  # Вязкость [сПз] = 10e-3 [Па * с]
compressibility = 5 * 10e-9  # [1/Па] сжимаемость
coef = - B * viscosity / 2 / np.pi / permeability / h # вспомогательный коэффициент
dt = 1  # шаг по времени в сутках

eta = 1.0
pressure_start = np.full((Nx, Ny), 0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0

pressure, pressure_w = solve_for_one_well_implicit(X, Y, x_w, y_w, q_injection, r_w, coef, pressure_start, T, dt, eta)

# Визуализация распределения давления
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
plt.colorbar(label='Давление')
plt.title(f'Распределение давления в момент времени {T}')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

