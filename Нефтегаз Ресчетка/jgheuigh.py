import numpy as np
import matplotlib.pyplot as plt

# Определение смещения
x_0 = 2.0
y_0 = 3.0

# Определение размеров и шагов сетки
N_x = 10
N_y = 10
Delta_x = 1
Delta_y = 1

# Создание сетки в декартовой системе координат
x_values = np.arange(0, N_x * Delta_x, Delta_x)
y_values = np.arange(0, N_y * Delta_y, Delta_y)

# Генерация массива точек в декартовой системе координат
X, Y = np.meshgrid(x_values, y_values)

# Преобразование в полярные координаты со смещением
X_shifted = X - x_0
Y_shifted = Y - y_0
r_values = np.sqrt(X_shifted ** 2 + Y_shifted ** 2)
theta_values = np.arctan2(Y_shifted, X_shifted)

# Преобразование обратно в декартовы координаты со смещением
X_back = r_values * np.cos(theta_values) + x_0
Y_back = r_values * np.sin(theta_values) + y_0

# Построение графика в полярной системе координат
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(theta_values, r_values, color='blue')
ax.set_title('Сетка в полярной системе координат')
plt.show()

# Построение графика в декартовой системе координат
fig, ax = plt.subplots()
ax.scatter(X, Y, color='blue', label='Исходная сетка')
ax.scatter(X_back, Y_back, color='red', label='Восстановленная сетка')
ax.set_title('Сетка в декартовой системе координат')
ax.legend()
plt.show()
