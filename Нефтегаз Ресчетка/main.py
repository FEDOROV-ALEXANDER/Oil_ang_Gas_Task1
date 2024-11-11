import matplotlib.pyplot as plt
import pandas as pd
import math as m
from well import Well
import numpy as np
import time as t
import Results as r


def choose_step(length, width, x_wells, y_wells):
    step =  m.gcd(length, *x_wells), m.gcd(width, *y_wells)
    step = m.gcd(step[0], step[1])
    return step, step


# данные для скважин скважины
wells = [
    Well(1000, 1000, 1.5, 800, 1),
    Well(1700, 1700, 1.5, 1000, 2),
    Well(2100, 1000, 1.5, -700, 3),
    Well(800, 1800, 1.5, -800, 4),

]

# Ввод входных значений
length, width = 2500, 2500  # [м] геометрические размеры рассчитываемой области
dx, dy = choose_step(length, width, [well.x_w for well in wells],
                     [well.y_w for well in wells])  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1  # количество элементов
X = np.linspace(0, length, Nx)
Y = np.linspace(0, width, Ny)
T = 365 * 1  # время работы в сутках

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

print(eta_matrix.mean())
r.permability_graph(X, Y, permeability_matrix)

for well in wells:
    if well.q <= 0:
        plt.scatter(well.x_w, well.y_w, marker='x', color='black', s=50 )
    else:
        plt.scatter(well.x_w, well.y_w,marker='v', color='black', s=50 )
plt.colorbar()
plt.show()
from Solve import solve_for_one_well_explicit

begin = t.time()
for well in wells:
    history = []
    # Используем явный метод
    well.pressure_field, well.pressure_well, well.productivity, well.time_well, well.history = solve_for_one_well_explicit(
        X.copy(), Y.copy(), well.x_w, well.y_w, well.q, well.r_w, coef_matrix, pressure_start.copy(), T, eta_matrix)
    pressure += well.pressure_field
    history += well.history
print(t.time() - begin)


data = []

# Проход по каждому массиву в history
for i, array in enumerate(history):
    # Развертывание каждого двумерного массива в одномерный
    flattened_array = array.flatten()
    # Добавление номера массива и его размеров
    array_with_index = np.insert(flattened_array, 0, [i, array.shape[0], array.shape[1]])
    # Добавление в общий список
    data.append(array_with_index)

# Создание DataFrame
df = pd.DataFrame(data)

df.to_excel('history_field_pressure.xlsx', index=False)


wells_df = []
for well in wells:
    well_df = pd.DataFrame({
        'well_id': well.number ,
        'well_time': well.time_well,
        'well_productivity': well.productivity,
        'pressure_well': well.pressure_well,
    })
    wells_df.append(well_df)
combinet_df = pd.concat(wells_df, ignore_index=True)

combinet_df.to_excel('well_information.xlsx', index=False)


# last_array_number = len(history) - 1
# pressure = r.get_2d_array(df, last_array_number)
# X, Y = np.meshgrid(np.arange(pressure.shape[1]), np.arange(pressure.shape[0]))

r.pressure_result(X, Y, pressure)
r.pressure_on_wells(wells)
r.productivity(wells)

r.create_pressure_slider(df, history)
