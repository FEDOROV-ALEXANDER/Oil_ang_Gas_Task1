import numpy as np
import matplotlib.pyplot as plt

def create_refined_grid(x_grid, y_grid, x_refine, y_refine, refine_radius, fine_step):
    # Создаем грубую сетку
    X_coarse, Y_coarse = np.meshgrid(x_grid, y_grid)

    # Создаем уточненную сетку вокруг точки (x_refine, y_refine)
    x_fine = np.arange(x_refine - refine_radius, x_refine + refine_radius, fine_step)
    y_fine = np.arange(y_refine - refine_radius, y_refine + refine_radius, fine_step)
    X_fine, Y_fine = np.meshgrid(x_fine, y_fine)

    # Объединяем грубую и уточненную сетки
    X = np.concatenate((X_coarse.flatten(), X_fine.flatten()))
    Y = np.concatenate((Y_coarse.flatten(), Y_fine.flatten()))

    # Удаляем дубликаты и сортируем
    X, Y = np.unique(X), np.unique(Y)

    # Создаем полную сетку
    X_full, Y_full = np.meshgrid(X, Y)


    return X_full, Y_full

# Параметры сетки
x_grid = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Неравномерная сетка по X
y_grid = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Неравномерная сетка по Y
x_refine, y_refine = 5, 5  # Точка, вокруг которой будет уточнение
refine_radius = 2  # Радиус уточнения
fine_step = 0.1  # Шаг уточненной сетки

# Создаем сетку с уточнением
X, Y = create_refined_grid(x_grid, y_grid, x_refine, y_refine, refine_radius, fine_step)

# Визуализация сетки
plt.scatter(X, Y, s=1)
plt.scatter(x_refine, y_refine, color='red', s=10)  # Отмечаем точку уточнения
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Local Grid Refinement')
plt.show()