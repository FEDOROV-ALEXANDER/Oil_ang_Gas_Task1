import numpy as np
import random


def generate_permeability_matrix(X, Y, permeability, type_number):
    Nx, Ny = len(X), len(Y)
    # np.random.seed(0)
    permeability_matrix = np.full((Nx, Ny), permeability)

    if type_number == 1:
        # Квадрат
        center_x, center_y = Nx // 2, Ny // 2
        square_size = 200
        permeability_matrix[center_x - square_size // 2:center_x + square_size // 2,
        center_y - square_size // 2:center_y + square_size // 2] = permeability * 2
    elif type_number == 2:
        # Круг
        center_x, center_y = Nx // 2, Ny // 2
        radius = 200
        for i in range(Nx):
            for j in range(Ny):
                if (i - center_x) ** 2 + (j - center_y) ** 2 <= radius ** 2:
                    permeability_matrix[i, j] = permeability * 2
    elif type_number == 3:
        # Неровное что-то
        num_lines = 8
        line_thickness = 7
        for line_index in range(num_lines):
            start_x, start_y = 0, Ny // 2 + line_index * (Ny // (num_lines + 1))
            end_x, end_y = Nx - 1, Ny // 2 + line_index * (Ny // (num_lines + 1))
            current_x, current_y = start_x, start_y
            while current_x < end_x:
                for dy in range(-line_thickness // 2, line_thickness // 2 + 1):
                    if 0 <= current_y + dy < Ny:
                        permeability_matrix[:current_x, current_y + dy] = permeability * 2
                current_x += 1
                current_y += random.randint(-1, 1)
                current_y = max(0, min(current_y, Ny - 1))
            for dy in range(-line_thickness // 2, line_thickness // 2 + 1):
                if 0 <= current_y + dy < Ny:
                    permeability_matrix[current_x:, current_y + dy] = permeability * 2
    elif type_number == 4:
        # Линия неровная
        start_x, start_y = 0, Ny // 2
        end_x, end_y = Nx - 1, Ny // 2
        current_x, current_y = start_x, start_y
        while current_x < end_x:
            permeability_matrix[current_x, current_y] = permeability * 2
            current_x += 1
            current_y += random.randint(-1, 1)
            current_y = max(0, min(current_y, Ny - 1))
    elif type_number == 5:
        # Линия синус
        amplitude = 20
        frequency = 0.1
        for i in range(Nx):
            j = int(Ny // 2 + amplitude * np.sin(frequency * i))
            permeability_matrix[i, j] = permeability * 2
    elif type_number == 6:
        # Рандомное
        half_elements = (Nx * Ny) // 2
        indices = np.random.choice(Nx * Ny, half_elements, replace=False)
        permeability_matrix.flat[indices] = permeability * 2
    elif type_number == 7:
        # Половинка
        permeability_matrix[:, :Ny//2] = permeability * 2
    elif type_number == 8:
        # Эллипс
        center_x, center_y = Nx // 2, Ny // 2
        radius = 200
        for i in range(Nx):
            for j in range(Ny):
                if 2*(i - center_x) ** 2 + (j - center_y) ** 2 <= radius ** 2:
                    permeability_matrix[i, j] = permeability * 2
    else:
        raise ValueError("Неверный номер типа. Допустимые значения: 1-7.")

    return permeability_matrix
