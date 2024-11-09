import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt


def pressure_result(X, Y,  pressure):
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
            plt.legend(f'Продуктивность {well.number} скважины')
    plt.xlabel('Время, сут')
    plt.ylabel('Продуктивность, м3/Бар')
    plt.show()
