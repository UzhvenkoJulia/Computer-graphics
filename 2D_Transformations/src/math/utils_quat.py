import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.utils_matrix import is_orthogonal


def euler_xyz_to_quaternion(phi, theta, psi):
    """Обчислює кватерніон для кутів Ейлера (XYZ)."""
    cos_phi, sin_phi = np.cos(phi / 2), np.sin(phi / 2)
    cos_theta, sin_theta = np.cos(theta / 2), np.sin(theta / 2)
    cos_psi, sin_psi = np.cos(psi / 2), np.sin(psi / 2)

    return Quaternion(
        cos_phi * cos_theta * cos_psi - sin_phi * sin_theta * sin_psi,
        sin_phi * cos_theta * cos_psi + cos_phi * sin_theta * sin_psi,
        cos_phi * sin_theta * cos_psi - sin_phi * cos_theta * sin_psi,
        cos_phi * cos_theta * sin_psi + sin_phi * sin_theta * cos_psi
    )

def quaternion_to_euler_xyz(quat):
    return phi, theta, psi  # TODO:


def slerp(q0: Quaternion, q1: Quaternion, t):
    """
    Виконує сферичну лінійну інтерполяцію (SLERP) між двома кватерніонами q0 і q1.

    Параметри:
    q0, q1 : Quaternion - початковий та кінцевий кватерніони
    t : float - параметр інтерполяції (0 ≤ t ≤ 1)

    Повертає:
    Інтерпольований кватерніон Quaternion
    """

    dot = q0.toVec4() * q1.toVec4()

    # Якщо косинус від'ємний, змінюємо знак одного кватерніона (коротший шлях)
    if dot < 0.0:
        q1 = -q1
        dot = -dot

    # Якщо кватерніони майже однакові, використовуємо лінійну інтерполяцію
    if dot > 0.9995:
        result = q0 * (1 - t) + q1 * t
        return result.normalized()  # Нормалізація

    # Обчислення кута між кватерніонами
    theta_0 = np.arccos(dot)
    sin_theta_0 = np.sin(theta_0)

    # Вагові коефіцієнти
    s0 = np.sin((1 - t) * theta_0) / sin_theta_0
    s1 = np.sin(t * theta_0) / sin_theta_0

    # SLERP інтерполяція
    return q0 * s0 + q1 * s1


def rotation_matrix_to_quaternion(r):
    """
    Конвертує матрицю обертання у кватерніон Quaternion = (q0, q1, q2, q3).

    Параметри:
    r - ортонормована матриця обертання

    Повертає:
    Quaternion - кватерніон у форматі (q0, q1, q2, q3).
    """

    if not is_orthogonal(r):
        raise ValueError("Матриця обертання не є ортогональною!")

    r = Mat4x4(r)

    # Обчислення сліду матриці
    trace = r[0, 0] + r[1, 1] + r[2, 2]

    print(f"trace={trace}, diag=({r[0, 0]}, {r[1, 1]}, {r[2, 2]})")
    if trace >= 0:
        # print(f"Case 0")
        q0 = 1 / 2.0 * np.sqrt(1.0 + trace)
        q1 = 1 / (4.0 * q0) * (r[2, 1] - r[1, 2])
        q2 = 1 / (4.0 * q0) * (r[0, 2] - r[2, 0])
        q3 = 1 / (4.0 * q0) * (r[1, 0] - r[0, 1])
    elif (r[0, 0] > r[1, 1]) and (r[0, 0] > r[2, 2]):
        # print(f"Case 1")
        q1 = 1 / 2.0 * np.sqrt(1.0 + r[0, 0] - r[1, 1] - r[2, 2])
        q0 = 1 / (4.0 * q1) * (r[2, 1] - r[1, 2])
        q2 = 1 / (4.0 * q1) * (r[0, 1] + r[1, 0])
        q3 = 1 / (4.0 * q1) * (r[0, 2] + r[2, 0])
    elif r[1, 1] > r[2, 2]:
        # print(f"Case 2")
        q2 = 1 / 2.0 * np.sqrt(1.0 - r[0, 0] + r[1, 1] - r[2, 2])
        q0 = 1 / (4.0 * q2) * (r[0, 2] - r[2, 0])
        q1 = 1 / (4.0 * q2) * (r[0, 1] + r[1, 0])
        q3 = 1 / (4.0 * q2) * (r[1, 2] + r[2, 1])
    else:
        # print(f"Case 3")
        q3 = 1 / 2.0 * np.sqrt(1.0 + r[2, 2] - r[0, 0] - r[1, 1])
        q0 = 1 / (4.0 * q3) * (r[1, 0] - r[0, 1])
        q1 = 1 / (4.0 * q3) * (r[0, 2] + r[2, 0])
        q2 = 1 / (4.0 * q3) * (r[1, 2] + r[2, 1])

    return Quaternion(q0, q1, q2, q3)


if __name__ == '__main__':
    phi, theta, psi = np.radians(32), np.radians(45), np.radians(44)

    Rx = Mat4x4.rotation_x(phi)
    Ry = Mat4x4.rotation_y(theta)
    Rz = Mat4x4.rotation_z(psi)
    R_final = Rx * Ry * Rz

    qi = Quaternion.rotation_x(phi)
    qj = Quaternion.rotation_y(theta)
    qk = Quaternion.rotation_z(psi)
    q = qi * qj * qk
    print(q)
    q_euler = euler_xyz_to_quaternion(phi, theta, psi)
    print(q_euler)
    print(q_euler - q)

    # u = Vec4(1, 0, 0)
    # print(u)
    # w = q.rotate_vector(u)
    # print(w)

    q0 = Quaternion.rotation_y(phi)
    q1 = Quaternion.rotation_y(2 * phi)
    print("======================")
    print(q0)
    print(q1)
    print("======================")

    T = 10
    for i in range(T + 1):
        qt = slerp(q0, q1, i / T)
        # print(qt, qt.norm())
        print(qt)

    print("======== Rotation to quaternion ======\n\n")
    print(q)
    print(q_euler)

    q_from_matrix = rotation_matrix_to_quaternion(R_final)
    print(q_from_matrix)
