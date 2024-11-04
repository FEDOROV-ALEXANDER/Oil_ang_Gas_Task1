import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ввод входных значений
length, width = 15000, 15000  # [м] геометрические размеры рассчитываемой области
dx, dy = 100, 100  # [м] шаг по направлениям
Nx, Ny = int(length / dx) + 1, int(width / dy) + 1 # количество элементов
# x = np.linspace(0, length, Nx)
# y = np.linspace(0, width, Ny)
x, y = np.meshgrid(np.linspace(0, length, Nx), np.linspace(0, width, Ny))

# координаты скважины
x_w = 1000
y_w = 1000

# пока будет одна скважина, нагнетательная
q_injection = 10  # [м3/сут] дебит нагнетательных скважин




# TODO надо разобраться с тензором проницаемости. Пока задаю одинаковым во всех направлениях для каждого объема
# То есть это будет скаляр. Потом надо будет сделать 2 области с разным коэффициентами, после уже задавать тензор в каждом объеме

permeability = 1  # [мД] проницаемость - скаляр
permeability_field = np.full((Nx, Ny), permeability)  # проницаемость по расчетной области

# параметры взяты плюс-минус от балды
viscosity = 1  # Вязкость [сПз] = 10e-3 [Па * с]
compressibility = 5 * 10e-9  # [1/Па] сжимаемость

dt = 1  # шаг по времени в сутках

# Начальные и граничные условия: давление нулевое, пласт бесконечный -> давление на границах 0
# TODO разобраться, какое значение брать у потенциала Ф, на 117 странице Лэйка1_B он взят постоянным, но хз насколько так можно, потому что он определяется как разность давления жидкости и градиента давления под действием силы тяжести

# Сначала сделаю явную схему интегрирования, потому что как то не доходит прикол решения методом прогонки: единственное что смог найти это про построение 5 диагональной матрицы
def solve_for_one_well(x, y, x_w, y_w, q, p_field_initial):
    # преобразование координат так, чтобы в начале координат была скважина
    x_shifted = x - x_w
    y_shifted = x - y_w
    r_values = np.sqrt(x_shifted ** 2 + y_shifted ** 2)
    theta_values = np.arctan2(x_shifted, x_shifted)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.scatter(theta_values, r_values, color='blue')
    ax.set_title('Сетка в полярной системе координат')
    plt.show()
    # начальные условия
    p_field = p_field_initial
    # граничные условия на внешней границе
    p_field[:, 0 ] = 0
    p_field[:, -1] = 0
    p_field[0, :] = 0
    p_field[-1, :] = 0
    # Граничные условия на забое скважины

solve_for_one_well(x, y, x_w, y_w, q_injection, p_field_initial=np.zeros((Nx, Ny)))