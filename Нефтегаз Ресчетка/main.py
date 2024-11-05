import numpy as np
from Solve import solve_for_one_well
import matplotlib.pyplot as plt
import seaborn as sns
# TODO теперь надо постараться реализовать для нескольких скважин
# TODO реализовать неявный метод
# TODO реализовать увеличение картинки (отрисовка ее части) около скважины
# TODO подумать на счет создания классов для скважин, так будет удобнее наверное
# Ввод входных значений
length, width = 10000, 10000  # [м] геометрические размеры рассчитываемой области
dx, dy = 100, 100   # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 365

# координаты скважины
x_w = 300
y_w = 1300
r_w = 1.5
# пока будет одна скважина, нагнетательная
q_injection = 10  # [м3/сут] дебит нагнетательных скважин

B = 5  # Объемный коэффициент
h = 20  # толщина пласта

# параметры взяты плюс-минус от балды
viscosity = 1  # Вязкость [сПз] = 10e-3 [Па * с]
compressibility = 5 * 10e-9  # [1/Па] сжимаемость
permeability = 1  # [мД] проницаемость - скаляр
eta = 1.0
coef = - B * viscosity / 2 / np.pi / permeability / h  # вспомогательный коэффициент
dt = 1 / (2 * eta * (dx ** 2 + dy ** 2)) * dx ** 2 * dy ** 2 # шаг по времени в сутках c учетом устойчивости
if dt > 5: dt = 5

pressure_start = np.full((Nx, Ny), 0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0

pressure, pressure_w = solve_for_one_well(X, Y, x_w, y_w, q_injection, r_w, coef, pressure_start.copy(), T, dt, eta)

# Визуализация распределения давления
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
plt.colorbar(label='Давление')
plt.title(f'Распределение давления через {T} дней')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
