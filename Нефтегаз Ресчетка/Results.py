import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def permeability(X, Y, permeability_matrix, wells):
    plt.style.use('dark_background')
    plt.figure()
    plt.title('Распределение проницаемости')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.pcolormesh(X, Y, permeability_matrix)
    for well in wells:
        if well.q <= 0:
            plt.scatter(well.x_w, well.y_w, marker='x', color='black', s=50)
        else:
            plt.scatter(well.x_w, well.y_w, marker='v', color='black', s=50)
    plt.colorbar()
    plt.savefig('results files/проницаемость.png', dpi=1000)
    plt.show()


def pressure_result(X, Y, pressure):
    # for style in plt.style.available == dark_background:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
    cbar = plt.colorbar(cax, label='Изменение давления, бар')
    ax.set_title(f'Распределение давления')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.savefig('results files/результат_давление.png', dpi=1000)
    plt.show()


# def pressure_history():


def pressure_on_wells(wells):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
    for well in wells:
        ax.plot(well.time_well, well.pressure_well)
    ax.set_xlabel('Время, сут')
    ax.set_title('Давление на забоях скважины')
    ax.set_ylabel('Давление на забоях скважин, Бар')
    ax.legend([f' {well.number} скважина c дебитом {well.q} ' for well in wells])
    plt.savefig('results files/давление_забой.png', dpi=1000)
    plt.show()


def productivity(wells):
    labels = []
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
    ax.set_title('Продуктивность добывающих скважин')
    for well in wells:
        if well.q <= 0:
            label = f'{well.number} скважина с дебитом {-well.q} м3/сут'
            ax.plot(well.time_well, well.productivity)
            labels.append(label)
    ax.legend(labels)
    ax.set_xlabel('Время, сут')
    ax.set_ylabel('Продуктивность, м3/Бар')
    plt.savefig('results files/продуктивность.png', dpi=1000)
    plt.show()


# Проход по каждому массиву в history
def save_data(history, wells):
    data = []
    for i, array in enumerate(history):
        # Развертывание каждого двумерного массива в одномерный
        flattened_array = array.flatten()
        # Добавление номера массива и его размеров
        array_with_index = np.insert(flattened_array, 0, [i, array.shape[0], array.shape[1]])
        # Добавление в общий список
        data.append(array_with_index)

    # Создание DataFrame
    df = pd.DataFrame(data)

    df.to_excel('results files/history_field_pressure.xlsx', index=False)

    wells_df = []
    for well in wells:
        well_df = pd.DataFrame({
            'well_id': well.number,
            'well_time': well.time_well,
            'well_productivity': well.productivity,
            'pressure_well': well.pressure_well,
        })
        wells_df.append(well_df)
    combinet_df = pd.concat(wells_df, ignore_index=True)

    combinet_df.to_excel('results files/well_information.xlsx', index=False)