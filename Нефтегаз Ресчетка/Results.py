import matplotlib.pyplot as plt
import pandas as pd

def get_2d_array(df, array_number):
    # Извлечение строки с нужным номером массива
    row = df[df[0] == array_number]
    if not row.empty:
        # Извлечение размеров массива и преобразование их в целые числа
        rows, cols = int(row.iloc[0, 1]), int(row.iloc[0, 2])
        # Извлечение данных массива
        array_data = row.iloc[0, 3:].values
        # Восстановление двумерного массива
        return array_data.reshape(rows, cols)
    else:
        return None

def create_pressure_slider(df, history):
    # Создаем слайдер для отображения каждого 100-го массива
    steps = []
    for i in range(0, len(history), 100):
        pressure = get_2d_array(df, i)
        X, Y = np.meshgrid(np.arange(pressure.shape[1]), np.arange(pressure.shape[0]))

        step = dict(
            method="update",
            args=[{"z": [pressure]}, {"title": f"Распределение давления (Шаг {i})"}],
            label=str(i)
        )
        steps.append(step)

    # Создаем начальный график
    initial_pressure = get_2d_array(df, 0)
    X, Y = np.meshgrid(np.arange(initial_pressure.shape[1]), np.arange(initial_pressure.shape[0]))

    fig = px.imshow(initial_pressure, color_continuous_scale='Viridis')

    fig.update_layout(
        title='Распределение давления (Шаг 0)',
        xaxis_title='X',
        yaxis_title='Y',
        sliders=[dict(
            active=0,
            steps=steps
        )]
    )

    # fig.write_image('Распределение давления.svg', format='svg')
    fig.show()


def permability_graph(X, Y, permeability_matrix):
    plt.style.use('dark_background')
    plt.figure()
    plt.title('Распределение проницаемости')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.pcolormesh(X, Y, permeability_matrix)

def pressure_result(X, Y, pressure):
    # for style in plt.style.available == dark_background:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.pcolormesh(X, Y, pressure, shading='auto', cmap='viridis')
    cbar = plt.colorbar(cax, label='Изменение давления, бар')
    ax.set_title(f'Распределение давления')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Явный')
    plt.show()


# def pressure_history():


def pressure_on_wells(wells):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'hspace': 0})
    for well in wells:
        ax.plot(well.time_well, well.pressure_well)
    ax.set_xlabel('Время, сут')
    ax.set_title('Явный')
    ax.set_ylabel('Давление на забоях скважин, Бар')
    ax.legend([f' {well.number} скважина c дебитом {well.q} ' for well in wells])
    plt.show()


def productivity(wells):
    plt.style.use('dark_background')
    plt.figure()
    for well in wells:
        if well.q <= 0:
            plt.plot(well.time_well, well.productivity)
            plt.legend('{} скважина с дебитом {}'.format(well.number, well.q))
    plt.xlabel('Время, сут')
    plt.ylabel('Продуктивность, м3/Бар')
    plt.show()