import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import is_same_matrix


def euler_zxz_rotation_matrix(phi, theta, psi):
    """
    Generates a rotation matrix from Euler angles (ZXZ configuration) without matrix multiplication.

    Input:
    - alpha: rotation angle around the Z axis
    - beta: rotation angle around the new X axis
    - gamma: rotation angle around the new Z axis

    Output:
    - 3x3 rotation matrix
    """
    cos_varphi, sin_varphi = np.cos(phi), np.sin(phi)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_psi, sin_psi = np.cos(psi), np.sin(psi)

    return Mat4x4([
        [cos_varphi * cos_psi - sin_varphi * cos_theta * sin_psi,
         -cos_varphi * sin_psi - sin_varphi * cos_theta * cos_psi, sin_varphi * sin_theta],
        [sin_varphi * cos_psi + cos_varphi * cos_theta * sin_psi,
         -sin_varphi * sin_psi + cos_varphi * cos_theta * cos_psi, -cos_varphi * sin_theta],
        [sin_theta * sin_psi, sin_theta * cos_psi, cos_theta]
    ])




if __name__ == '__main__':

    phi, theta, psi = np.radians(-80), np.radians(13), np.radians(145)


    M1 = Mat4x4.rotation_euler(phi, theta, psi, "ZXZ")
    M3 = euler_zxz_rotation_matrix(phi, theta, psi)

    phi3, theta3, psi3 = Mat4x4.toEuler(M1, "ZXZ")
    M2 = Mat4x4.rotation_euler(phi3, theta3, psi3, "ZXZ")

    print("Euler base: ", np.degrees(phi), np.degrees(theta), np.degrees(psi))
    print("Euler calc: ", np.degrees(phi3), np.degrees(theta3), np.degrees(psi3))

    print("=== ====")
    print(M1)
    print("=== ====")
    print(M3)
    print(f"Matrix the same {is_same_matrix(M1, M3)}")
    print(M2)
    print(f"Matrix the same {is_same_matrix(M1, M2)}")
