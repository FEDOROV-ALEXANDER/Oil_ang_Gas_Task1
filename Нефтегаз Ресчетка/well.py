import numpy as np


class Well:
    def __init__(self, x_w, y_w, r_w, q, number):
        self.x_w = x_w  # координата скважины по х
        self.y_w = y_w  # координата скважины по у
        self.r_w = r_w  # радиус скважины
        self.q = q  # постоянный дебит м3/сут
        self.pressure_well = np.empty((0, 0))
        self.pressure_field = np.empty((0, 0))
        self.time_well = np.empty((0, 0))
        self.number = number
        self.productivity = np.empty((0, 0))
        self.history = []

    def __str__(self):
        """
        Возвращает строковое представление объекта Скважина.
        """
        return f"Скважина(x_w={self.x_w}, y_w={self.y_w}, r_w={self.r_w}, q={self.q})"

    def __repr__(self):
        """
        Возвращает строковое представление объекта Скважина для отладки.
        """
        return self.__str__()
