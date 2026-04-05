import numpy as np

def translation_matrix2d(t_x, t_y):
    return np.array([
        [1, 0, t_x],
        [0, 1, t_y],
        [0, 0, 1]
    ])

def translation_matrix(t_x, t_y, t_z):
    return np.array([
        [1, 0, 0, t_x],
        [0, 1, 0, t_y],
        [0, 0, 1, t_z],
        [0, 0, 0,   1]
    ])


if __name__ == '__main__':
    # Зсуви
    T = translation_matrix(t_x=3,  # Зсув уздовж осі X
                           t_y=4,  # Зсув уздовж осі Y
                           t_z=5  # Зсув уздовж осі Z
                           )
    print(T)
