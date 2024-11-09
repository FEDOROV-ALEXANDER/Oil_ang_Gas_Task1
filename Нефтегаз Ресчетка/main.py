import numpy as np
from Solve import solve_for_one_well_explicit
import matplotlib.pyplot as plt
import math as m
from well import Well
import seaborn as sns


def choose_step(length, width, x_wells, y_wells):
    dx, dy = m.gcd(length, *x_wells), m.gcd(width, *y_wells)
    return dx, dy


# данные для скважин скважины
wells = [
    Well(2550, 2550, 1.5, 10, 1),
    Well(3700, 750, 1.5, 8, 2),
    Well(255, 755, 1.5, -14, 3),
    Well(1000, 3700, 1.5, -14, 4),
]


# Ввод входных значений
length, width = 4000, 4000  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well.x_w for well in wells],
                     [well.y_w for well in wells])  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 10 * 365

B = 1.2  # Объемный коэффициент
h = 10  # толщина пласта

# параметры взяты плюс-минус от балды
viscosity = 10  # Вязкость [сПз] = 10e-3 [Па * с]
compressibility = 5 * 10e-9  # [1/Па] сжимаемость
permeability = 100  # [мД] проницаемость - скаляр
eta = 1.0
coef = - B * viscosity / 2 / np.pi / permeability / h  # вспомогательный коэффициент

pressure_start = np.full((Nx, Ny), 0.0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0
pressure = pressure_start.copy()


for well in wells:
    # Используем явный метод
    well.pressure_field, well.pressure_well, well.time_well = solve_for_one_well_explicit(X.copy(), Y.copy(), well.x_w,
                                                                                          well.y_w, well.q, well.r_w,
                                                                                          coef, pressure_start.copy(),
                                                                                          T, eta)

    pressure += well.pressure_field



fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
for well in wells:
    ax.plot(well.time_well, well.pressure_well)
ax.set_xlabel('Время')
ax.set_title('Явный')
ax.set_ylabel('Давление на забоях скважин')

ax.legend([f' {well.number} скважина c дебитом {well.q} ' for well in wells])
plt.show()


fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
cbar = plt.colorbar(cax, label='Давление')
ax.set_title(f'Распределение давления через {T} дней')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Явный')
plt.show()
