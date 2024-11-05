import numpy as np
import matplotlib.pyplot as plt

# Размеры сетки
Nx, Ny = 100, 100

# Создание сетки
x = np.linspace(0, 10, Nx)
y = np.linspace(0, 10, Ny)
X, Y = np.meshgrid(x, y)

# Создание матрицы давлений (изначально нулевая)
pressure = np.zeros((Ny, Nx))

# Преобразование декартовых координат в полярные
# Смещение центра полярной системы координат
center_x, center_y = 7, 2

# Расчет радиуса и угла
r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
theta = np.arctan2(Y - center_y, X - center_x)

# Расчет давления в полярной системе координат
pressure_polar = r**2

# Перевод давления обратно в декартову систему координат
pressure = pressure_polar

# Визуализация распределения давления
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
plt.colorbar(label='Давление')
plt.title('Распределение давления')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()