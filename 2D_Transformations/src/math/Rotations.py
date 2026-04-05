import numpy as np


def rotation_matrix_x(phi):
    """
    Формує матрицю обертання навколо осі X на заданий кут.

    Parameters:
    theta (float): Кут обертання у радіанах.

    Returns:
    numpy.ndarray: Матриця обертання 3x3.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)
    return np.array([
        [1,         0,            0, ],
        [0,    cos_phi,    -sin_phi, ],
        [0,    sin_phi,     cos_phi, ],
    ])


def rotation_matrix_y(phi):
    """
    Формує матрицю обертання навколо осі Y на заданий кут.

    Parameters:
    theta (float): Кут обертання у радіанах.

    Returns:
    numpy.ndarray: Матриця обертання 3x3.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)
    return np.array([
        [ cos_phi,     0,     sin_phi ],
        [       0,     1,           0 ],
        [-sin_phi,     0,     cos_phi ],
    ])

def rotation_matrix_z(phi):
    """
    Формує матрицю обертання навколо осі Z на заданий кут.

    Parameters:
    theta (float): Кут обертання у радіанах.

    Returns:
    numpy.ndarray: Матриця обертання 3x3.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)

    return np.array([
        [cos_phi,   -sin_phi,     0 ],
        [sin_phi,    cos_phi,     0 ],
        [      0,          0,     1 ],
    ])


def get_rotation_angle(matrix):
    # Перевірка ортогональності R
    if not np.allclose(np.dot(matrix.T, matrix), np.eye(2)) or not np.isclose(np.linalg.det(matrix), 1):
        raise ValueError("Матриця не є коректною матрицею повороту.")

    """
    Обчислює кут повороту (в радіанах) із 2D матриці повороту.
    """
    if matrix.shape != (2, 2) and matrix.shape != (3, 3):
        raise ValueError("Некоректна матриця повороту!")

    if matrix.shape == (3, 3):
        matrix = matrix[:2, :2]

    # Витягуємо значення sin і cos
    cos_theta = matrix[0, 0]
    sin_theta = matrix[1, 0]

    # Обчислення кута через arctan2
    angle = np.arctan2(sin_theta, cos_theta)
    return angle


# Приклад використання:
if __name__ == "__main__":
    euler_angles_45_45_30 = [45, 15, 30]
    x = np.radians(euler_angles_45_45_30[0])  # Кут у градусах конвертується в радіани
    y = np.radians(euler_angles_45_45_30[1])  # Кут у градусах конвертується в радіани
    z = np.radians(euler_angles_45_45_30[2])  # Кут у градусах конвертується в радіани

    Rx = rotation_matrix_x(x)
    Ry = rotation_matrix_y(y)
    Rz = rotation_matrix_z(z)

    print("\nМатриця обертання послідовно по кутах ейлера:")
    print()
    print(Rx @ Ry @ Rz)

