import numpy as np
from Solve import solve_for_one_well_implicit, solve_for_one_well_explicit
import matplotlib.pyplot as plt
import math as m
from well import Well
import time as tm
import seaborn as sns

# TODO теперь надо постараться реализовать для нескольких скважин
# TODO реализовать неявный метод
# TODO реализовать увеличение картинки (отрисовка ее части) около скважины
# TODO подумать на счет создания классов для скважин, так будет удобнее наверное
# TODO задать неоднородность
# TODO попробовать ускорить программу

def choose_step(length, width, x_wells, y_wells):
    dx, dy = (min(m.gcd(length, *x_wells), m.gcd(width, *y_wells)),
              min(m.gcd(length, *x_wells), m.gcd(width, *y_wells)))
    return dx, dy

# координаты скважины
well_1 = Well(10, 20, 1.5, 10)
well_2 = Well(10, 20, 1.5, 10)
well_3 = Well(10, 20, 1.5, 10)
well_4 = Well(10, 20, 1.5, 10)
well_1 = Well(10, 20, 1.5, 10)# well_2 = Well(10, 90, 1.5, 10)
# well_3 = Well(32, 16, 1.5, -10)
# well_4 = Well(45, 90, 1.5, -10)

# пока будет одна скважина, нагнетательная

# Ввод входных значений
length, width = 500, 500  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well_1.x_w, well_2.x_w, well_3.x_w, well_4.x_w],
                     [well_1.y_w, well_2.y_w, well_3.y_w, well_4.y_w])   # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 1000  # время в сутках

B = 1.2  # Объемный коэффициент
h = 10  # толщина пласта (м)

# параметры взяты плюс-минус от балды
viscosity = 1e-3  # Вязкость [Па * с]
compressibility = 5 * 1e-9  # [1/Па] сжимаемость
permeability = 1e-15  # [м²] проницаемость
eta = permeability / (viscosity * compressibility)  # коэффициент пьезопроводности (м²/с)
coef = - B * viscosity / 2 / np.pi / permeability / h  # вспомогательный коэффициент

pressure_start = np.full((Nx, Ny), 0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0

# Используем неявный метод
begin = tm.time()
pressure, pressure_w, t = solve_for_one_well_implicit(X.copy(), Y.copy(), well_1.x_w, well_1.y_w, well_1.q, well_1.r_w, coef, pressure_start.copy(), T, eta)
print(tm.time() - begin)
t = np.array(t)
pressure_w = np.array(pressure_w)
print(t.shape, pressure_w.shape)

# Визуализация распределения давления
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, pressure, shading='nearest', cmap='viridis')
plt.colorbar(label='Давление')
plt.title(f'Распределение давления через {T} дней')
plt.xlabel('X')
plt.title('Неявный')
plt.ylabel('Y')
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t, pressure_w)
plt.xlabel('Время (дни)')
plt.title('Неявный')
plt.ylabel('Давление на забое скважины')
plt.show()

# Используем явный метод
pressure, pressure_w, t = solve_for_one_well_explicit(X.copy(), Y.copy(), well_1.x_w, well_1.y_w, well_1.q, well_1.r_w, coef, pressure_start.copy(), T, eta)
t = np.array(t)
pressure_w = np.array(pressure_w)
print(t.shape, pressure_w.shape)

# Визуализация распределения давления
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
plt.colorbar(label='Давление')
plt.title(f'Распределение давления через {T} дней')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Явный')
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t, pressure_w)
plt.xlabel('Время (дни)')
plt.title('Явный')
plt.ylabel('Давление на забое скважины')
plt.show()