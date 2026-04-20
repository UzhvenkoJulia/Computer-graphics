import numpy as np


def normal2d(start, end=None):
    if end is None:
        direction = start
        direction = direction / np.linalg.norm(direction)  # Vector normalization

        # Compute perpendicular vector
        __perpendicular = np.array([-direction[1], direction[0]])
        return __perpendicular
    else:
        # Line direction vector
        direction = end - start
        return normal2d(direction)
