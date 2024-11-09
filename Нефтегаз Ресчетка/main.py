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
    Well(3550, 2500, 1.5, 800, 1),
    Well(250, 2000, 1.5, 1000, 2),
    Well(1700, 2200, 1.5, -700, 3),
    Well(300, 1000, 1.5, -400, 4),

]


# Ввод входных значений
length, width = 4000, 4000  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well.x_w for well in wells],
                     [well.y_w for well in wells])  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T =  365  # время работы в секундах

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
coef_matrix = B * viscosity / 2 / np.pi / permeability_matrix / h
eta_matrix = permeability_matrix / (porosity * compressibility * viscosity)
print(eta_matrix.mean())


begin = t.time()
for well in wells:
    # Используем явный метод
    well.pressure_field, well.pressure_well, well.time_well = solve_for_one_well_explicit(X.copy(), Y.copy(), well.x_w, well.y_w, well.q, well.r_w, coef_matrix, pressure_start.copy(), T, eta_matrix)
    pressure += well.pressure_field
print(t.time() - begin)


fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
for well in wells:
    ax.plot(well.time_well, well.pressure_well)
ax.set_xlabel('Время')
ax.set_title('Явный')
ax.set_ylabel('Давление на забоях скважин')
ax.legend([f' {well.number} скважина c дебитом {well.q} ' for well in wells])
plt.show()

#for style in plt.style.available == dark_background:
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
cbar = plt.colorbar(cax, label='Давление')
ax.set_title(f'Распределение давления через {T} дней')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Явный')
plt.show()
print("nvnn")
