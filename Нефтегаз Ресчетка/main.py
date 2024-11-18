from Solve import  solve_for_one_well_explicit
import math as m
from well import Well
import numpy as np
import time as t
import Results as r



# TODO переписать функции решения в метод класса, потому что так удобнее наверное будет
# TODO попробовать поковыряться с сеткой, в том числе метод Форчуна
# TODO справить main файл и в результатах



def choose_step(length, width, x_wells, y_wells):
    step = m.gcd(length, *x_wells), m.gcd(width, *y_wells)
    step = m.gcd(step[0], step[1])
    return step, step


# данные для скважин скважины
wells = [
    Well(1000, 1000, 1.5, 1100, 1),
    Well(1710, 1705, 1.5, 1000, 2),
    Well(2100, 1050, 1.5, -1000, 3),
    Well(800, 1800, 1.5, -800, 4),
]

# Ввод входных значений
length, width = 2500, 2500  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well.x_w for well in wells],
                     [well.y_w for well in wells])  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 365 * 2  # время работы в сутках

B = 1.2  # Объемный коэффициент
h = 10  # толщина пласта

# параметры взяты плюс-минус от балды
viscosity = 10 * 10e-7 / 24 / 60 / 60  # Вязкость [Бар * сут]
compressibility = 5 * 10e-5  # [1/Бар] сжимаемость
permeability = 100 * 10e-16  # [м2] проницаемость
porosity = 0.05
eta = permeability / (porosity * compressibility * viscosity)

pressure_start = np.full((Nx, Ny), 0.0)
pressure_start[0, :] = 0
pressure_start[-1, :] = 0
pressure_start[:, 0] = 0
pressure_start[:, -1] = 0
pressure = pressure_start.copy()
permeability_matrix = np.full((Nx, Ny), permeability)
permeability_matrix[:Nx // 2, :] = permeability * 2

#  Тут можно создать рандомный разброс индексов
# half_elements = (Nx * Ny) // 2
# indices = np.random.choice(Nx * Ny, half_elements, replace=False)
# permeability_matrix.flat[indices] = permeability * 2

coef_matrix = B * viscosity / 2 / np.pi / permeability_matrix / h
eta_matrix = permeability_matrix / (porosity * compressibility * viscosity)

for well in wells:
    history = []
    # Используем явный метод
    well.pressure_field, well.pressure_well, well.productivity, well.time_well, well.history = solve_for_one_well_explicit(
        X.copy(), Y.copy(), well.x_w, well.y_w, well.q, well.r_w, coef_matrix, pressure_start.copy(), T, eta_matrix)
    pressure += well.pressure_field
    history += well.history

# r.save_data(history, wells)
r.permeability(X, Y, permeability_matrix, wells)
r.pressure_on_wells(wells)
r.productivity(wells)
r.pressure_result(X, Y, pressure)


