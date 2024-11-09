from matplotlib.pyplot import legend

from Solve import solve_for_one_well_explicit
import matplotlib.pyplot as plt
import math as m
from well import Well
import numpy as np
import seaborn as sns
import time as t

def choose_step(length, width, x_wells, y_wells):
    dx = dy = min(m.gcd(length, *x_wells), m.gcd(width, *y_wells))
    return dx, dy



# данные для скважин скважины
wells = [
    Well(1000, 1725, 1.5, 800, 1),
    Well(750, 1500, 1.5, 1000, 2),
    Well(1000, 1000, 1.5, -700, 3),
    Well(1700, 1700, 1.5, -400, 4),

]


# Ввод входных значений
length, width = 2500, 2500  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well.x_w for well in wells],
                     [well.y_w for well in wells])  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T =  365 * 10  # время работы в сутках

B = 1.2  # Объемный коэффициент
h = 10  # толщина пласта

# параметры взяты плюс-минус от балды
viscosity = 10 * 10e-7 / 24 /60 /60  # Вязкость [Бар * сут]
compressibility = 5 * 10e-5  # [1/Бар] сжимаемость
permeability = 100 * 10e-16  # [м2] проницаемость
porosity = 0.05
eta = permeability/ (porosity * compressibility * viscosity)

pressure_start = np.full((Nx, Ny), 0.0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0
pressure = pressure_start.copy()
permeability_matrix = np.full((Nx, Ny), permeability)
permeability_matrix[:Nx//2, :] = permeability * 2

#  Тут можно создать рандомный разброс индексов
# half_elements = (Nx * Ny) // 2
# indices = np.random.choice(Nx * Ny, half_elements, replace=False)
# permeability_matrix.flat[indices] = permeability * 2

coef_matrix = B * viscosity / 2 / np.pi / permeability_matrix / h
eta_matrix = permeability_matrix / (porosity * compressibility * viscosity)
print(eta_matrix.mean())

plt.figure()
plt.title('Распределение проницаемости')
plt.xlabel('x')
plt.ylabel('y')
plt.pcolormesh(X, Y, permeability_matrix)
plt.colorbar()
plt.show()



begin = t.time()
for well in wells:
    # Используем явный метод
    well.pressure_field, well.pressure_well, well.productivity,  well.time_well = solve_for_one_well_explicit(X.copy(), Y.copy(), well.x_w, well.y_w, well.q, well.r_w, coef_matrix, pressure_start.copy(), T, eta_matrix)
    pressure += well.pressure_field
print(t.time() - begin)


fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
for well in wells:
    ax.plot(well.time_well, well.pressure_well)
ax.set_xlabel('Время, сут')
ax.set_title('Явный')
ax.set_ylabel('Давление на забоях скважин, Бар')
ax.legend([f' {well.number} скважина c дебитом {well.q} ' for well in wells])
plt.show()

#for style in plt.style.available == dark_background:
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
cbar = plt.colorbar(cax, label='Изменение давления, бар')
ax.set_title(f'Распределение давления через {T} дней')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Явный')
plt.show()

plt.figure()
for well in wells:
    if well.q <=0:
        plt.plot(well.time_well, well.productivity)
        plt.legend(f'Продуктивность {well.number} скважины')
plt.xlabel('Время, сут')
plt.ylabel('Продуктивность, м3/Бар')
plt.show()
