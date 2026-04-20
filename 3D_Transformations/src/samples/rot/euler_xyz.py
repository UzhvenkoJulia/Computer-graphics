import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import is_same_matrix


def euler_xyz_rotation_matrix(phi, theta, psi):
    """
    Generates a rotation matrix from Euler angles (XYZ configuration) without matrix multiplication.

    Input:
    - phi: rotation angle around the X axis
    - theta: rotation angle around the Y axis
    - psi: rotation angle around the Z axis

    Output:
    - 3x3 rotation matrix
    """
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_psi, sin_psi = np.cos(psi), np.sin(psi)

    return Mat4x4(
        np.array([
            [cos_theta * cos_psi, -cos_theta * sin_psi, sin_theta],
            [cos_phi * sin_psi + sin_phi * sin_theta * cos_psi, cos_phi * cos_psi - sin_phi * sin_theta * sin_psi,
             -sin_phi * cos_theta],
            [sin_phi * sin_psi - cos_phi * sin_theta * cos_psi, sin_phi * cos_psi + cos_phi * sin_theta * sin_psi,
             cos_phi * cos_theta]
        ])
    )


if __name__ == '__main__':

    phi, theta, psi = np.radians(230), np.radians(-49), np.radians(145)
    M1 = Mat4x4.rotation_euler(phi, theta, psi, "XYZ")
    phi1, theta1, psi1 = Mat4x4.toEuler(M1, "xyz")

    M2 = Mat4x4.rotation_euler(phi1, theta1, psi1, "XYZ")

    print(M1)
    print()
    print(M2)
    print()

    print("Euler base: ", np.degrees(phi), np.degrees(theta), np.degrees(psi))
    print("Euler calc: ", np.degrees(phi1), np.degrees(theta1), np.degrees(psi1))
    print(f"MATRIX ARE THE SAME: {is_same_matrix(M1, M2)}")



