import numpy as np
import matplotlib.pyplot as plt


def create_refined_grid(x_min, x_max, y_min, y_max, x_refine, y_refine, refine_radius, coarse_step, fine_step):
    # Создаем грубую сетку
    x_coarse = np.arange(x_min, x_max, coarse_step)
    y_coarse = np.arange(y_min, y_max, coarse_step)
    X_coarse, Y_coarse = np.meshgrid(x_coarse, y_coarse)

    # Создаем уточненную сетку вокруг точки (x_refine, y_refine)
    x_fine = np.arange(x_refine - refine_radius, x_refine + refine_radius, fine_step)
    y_fine = np.arange(y_refine - refine_radius, y_refine + refine_radius, fine_step)
    X_fine, Y_fine = np.meshgrid(x_fine, y_fine)

    # Добавляем нулевые строки к меньшему массиву, чтобы их размеры совпадали
    if X_coarse.shape[0] > X_fine.shape[0]:
        X_fine = np.vstack([X_fine, np.zeros((X_coarse.shape[0] - X_fine.shape[0], X_fine.shape[1]))])
        Y_fine = np.vstack([Y_fine, np.zeros((Y_coarse.shape[0] - Y_fine.shape[0], Y_fine.shape[1]))])
    elif X_coarse.shape[0] < X_fine.shape[0]:
        X_coarse = np.vstack([X_coarse, np.zeros((X_fine.shape[0] - X_coarse.shape[0], X_coarse.shape[1]))])
        Y_coarse = np.vstack([Y_coarse, np.zeros((Y_fine.shape[0] - Y_coarse.shape[0], Y_coarse.shape[1]))])

    # Объединяем грубую и уточненную сетки
    X = np.concatenate((X_coarse, X_fine), axis=1)
    Y = np.concatenate((Y_coarse, Y_fine), axis=1)

    # Удаляем дубликаты и сортируем
    X, Y = np.unique(X), np.unique(Y)

    # Создаем полную сетку
    X_full, Y_full = np.meshgrid(X, Y)

    return X_full, Y_full


# Параметры сетки
x_min, x_max = 0, 10
y_min, y_max = 0, 10
x_refine, y_refine = 5, 5  # Точка, вокруг которой будет уточнение
refine_radius = 2  # Радиус уточнения
coarse_step = 1  # Шаг грубой сетки
fine_step = 0.1  # Шаг уточненной сетки

# Создаем сетку с уточнением
X, Y = create_refined_grid(x_min, x_max, y_min, y_max, x_refine, y_refine, refine_radius, coarse_step, fine_step)

# Визуализация сетки
plt.scatter(X, Y, s=1)
plt.scatter(x_refine, y_refine, color='red', s=10)  # Отмечаем точку уточнения
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Local Grid Refinement')
plt.show()