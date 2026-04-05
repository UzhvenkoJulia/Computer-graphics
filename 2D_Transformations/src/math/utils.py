import numpy as np


def normal2d(start, end=None):
    if end is None:
        direction = start
        direction = direction / np.linalg.norm(direction)  # Нормалізація вектора

        # Обчислення перпендикулярного вектора
        __perpendicular = np.array([-direction[1], direction[0]])
        return __perpendicular
    else:
        # Вектор напряму лінії
        direction = end - start
        return normal2d(direction)
