import numpy as np
from scipy.spatial.transform import Rotation
from scipy.spatial.transform import Rotation as R

from src.math.Mat3x3 import Mat3x3
from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Rotations import get_rotation_angle
from src.math.Vec3 import Vec3


def is_orthogonal(matrix, tol=1e-6):
    """
    Перевіряє, чи є матриця ортогональною (R^T * R = I).
    """
    matrix = Mat4x4(matrix)
    identity = Mat4x4()

    mul_mat = matrix.T * matrix
    return np.allclose(mul_mat.data, identity.data, atol=tol)

def is_same_matrix(matrix1, matrix2, tol=1e-6):
    """
    Перевіряє чи дві матриці однакові
    """
    matrix1 = Mat4x4(matrix1)
    matrix2 = Mat4x4(matrix2)
    mat_dif = matrix1 - matrix2

    return mat_dif.norm() < tol

# def decompose_affine(transition):
#
#     if not isinstance(transition, (np.ndarray, Mat4x4)):
#         raise TypeError("Transformation error.")
#
#     if isinstance(transition, Mat4x4):
#         transition = transition.data
#
#     if transition.shape != (4, 4):
#         raise ValueError("Матриця повинна бути розміром 4x4.")
#
#     # Виділення переносу
#     translation = transition[:3, 3]
#
#     # Виділення матриці RS
#     rs = transition[:3, :3]
#
#     # Обчислення масштабу
#     scale_x = np.linalg.norm(rs[:, 0])
#     scale_y = np.linalg.norm(rs[:, 1])
#     scale_z = np.linalg.norm(rs[:, 2])
#     scales = np.array([scale_x, scale_y, scale_z])
#
#     # Обчислення повороту
#     rotation = rs / scales
#
#     # # angle = get_rotation_angle(rotation)
#     #
#     # return translation, rotation, scales
#
#
#     # Полярна декомпозиція для коригування можливих викривлень
#     U, _, Vt = np.linalg.svd(rotation)
#     R = U @ Vt  # Чиста ортогональна матриця обертання
#
#     # Отримуємо вісь та кут повороту
#     rot = Rotation.from_matrix(R)
#     axis, angle = rot.as_rotvec(), np.degrees(rot.magnitude())
#
#     return T, scale_x, R, axis, angle


def decompose_translation_quaternion_scale(T):
    """
    Декомпозиція 4x4 матриці трансформації на компоненти:
    - Translation (зміщення)
    - Scale (розтяг)
    - Rotation (обертання у вигляді кватерніона)

    Вхід: 4x4 матриця T
    Вихід: translation, scale, quaternion
    """

    # 1. Витягнення зміщення (Translation)
    translation = T[:3, 3]

    # 2. Вилучення обертання та масштабування
    M = T[:3, :3]  # Верхня ліва 3x3 підматриця (містить масштаб та обертання)

    # 3. Обчислення масштабу (Scale)
    scale = np.linalg.norm(M, axis=0)  # Довжина кожного стовпця

    # 4. Отримання матриці обертання (нормалізація)
    R_matrix = M / scale  # Усунення впливу масштабу

    # 5. Конвертація матриці обертання у кватерніон
    quaternion = R.from_matrix(R_matrix).as_quat()  # Вихід: [x, y, z, w]

    quaternion = Quaternion(quaternion[3], *quaternion[:3])

    return translation, quaternion, scale


def decompose_affine(matrix):
    """
    Декомпозиція матриці 4x4 на трансляцію (T), масштабування (S) і обертання (R).
    """
    # Виділяємо трансляцію (остній стовпець без останнього елемента)
    T = matrix[:3, 3]

    # Виділяємо лінійне перетворення (верхня ліва 3x3 підматриця)
    M = matrix[:3, :3]

    # Отримуємо масштабування (довжини стовпців)
    S = np.linalg.norm(M, axis=0)

    # Нормалізуємо M, щоб прибрати масштабування і отримати чисте обертання
    R = M / S  # Ділимо кожен стовпець на відповідне значення масштабування

    # Полярна декомпозиція для коригування можливих викривлень
    U, _, Vt = np.linalg.svd(R)
    R = U @ Vt  # Чиста ортогональна матриця обертання

    # Отримуємо вісь та кут повороту
    rot = Rotation.from_matrix(R)
    # axis, angle = rot.as_rotvec(), np.degrees(rot.magnitude())
    axis, angle = rot.as_rotvec(), rot.magnitude()

    return T, R, S, axis, angle

def decompose_affine3(transition):

        if not isinstance(transition, (np.ndarray, Mat3x3)):
            raise TypeError("Transformation error.")

        if isinstance(transition, Mat3x3):
            transition = transition.data

        if transition.shape != (3, 3):
            raise ValueError("Матриця повинна бути розміром 3x3.")

        # Виділення переносу
        translation = transition[:2, 2]

        # Виділення матриці RS
        rs = transition[:2, :2]

        # Обчислення масштабу
        scale_x = np.linalg.norm(rs[:, 0])
        scale_y = np.linalg.norm(rs[:, 1])
        scales = np.array([scale_x, scale_y])

        # Обчислення повороту
        rotation = rs / scales

        angle = get_rotation_angle(rotation)

        return translation, angle, scales

