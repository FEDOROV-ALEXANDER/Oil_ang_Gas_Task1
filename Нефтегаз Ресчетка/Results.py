import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import imageio


def permeability(X, Y, permeability_matrix, wells):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))

    # Отображение проницаемости с помощью pcolormesh
    cax = ax.pcolormesh(X, Y, permeability_matrix, shading='auto', cmap='viridis')

    # Добавление цветовой шкалы
    cbar = plt.colorbar(cax, label='Проницаемость')

    # Добавление точек для скважин
    for well in wells:
        if well.q <= 0:
            ax.scatter(well.x_w, well.y_w, marker='x', color='black', s=50)
        else:
            ax.scatter(well.x_w, well.y_w, marker='v', color='black', s=50)

    # Настройка осей и заголовка
    ax.set_title('Распределение проницаемости')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Сохранение и отображение графика
    plt.savefig('results files/проницаемость.png', dpi=1000)
    plt.show()
    plt.close()


def pressure_result(X, Y, pressure):
    # for style in plt.style.available == dark_background:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
    cbar = plt.colorbar(cax, label='Изменение давления, бар')
    ax.set_title(f'Итоговое распределение давления')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.savefig('results files/результат_давление.png', dpi=1000)
    plt.show()
    plt.close()


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
    plt.close()


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
    plt.close()


def save_data(wells):
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


def pictures_for_gif(wells, X, Y, pressure_start):
    well = wells[0]
    history_summ_yield = np.zeros((well.pressure_field.shape[0], well.pressure_field.shape[1]))
    numbers = [round(i * (len(well.time_well) - 1) / 19) for i in range(20)]

    for number in numbers:
        for well in wells:
            history_summ_yield += well.history[number]
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 6))
        cax = ax.pcolormesh(X, Y, history_summ_yield - pressure_start, shading='auto', cmap='viridis')
        cbar = plt.colorbar(cax, label='Изменение давления, бар')
        ax.set_title(f'Распределение изменения давления через {int(well.time_well[number])} дней')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.savefig(f'results files/for gif pictures/давление {number} дни.png', dpi=1000)
        plt.close()
    return numbers


def gif_creating(wells, X, Y, pressure_start):
    numbers = pictures_for_gif(wells, X, Y, pressure_start)
    list = []
    for i in numbers:
        list.append('results files/for gif pictures/' + 'давление ' + str(i) + ' дни.png')
    with imageio.get_writer('results files/pressure_evolution.gif', mode='I', fps=1) as writer:
        for img in list:
            with Image.open(img) as im:
                writer.append_data(np.array(im))
