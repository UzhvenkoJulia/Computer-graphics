import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import is_same_matrix
from src.math.utils_quat import rotation_matrix_to_quaternion


def check(R):
    print("====================================================")

    quaternion = rotation_matrix_to_quaternion(R)
    M = quaternion.toRotationMatrix()

    is_same = is_same_matrix(M, R)
    if not is_same:
        print(f"ERRRRRRRRRRRORRR! {is_same}")
    else:
        print("OK")

    print(R)
    print(f"Quaternion 1: {quaternion}\n")
    print(f"Matrix from quaternion:\n")
    print(M)

    print()


if __name__ == '__main__':
    # Usage example
    Rx = Mat4x4.rotation_x(np.radians(30))
    Ry = Mat4x4.rotation_y(np.radians(40))
    Rz = Mat4x4.rotation_z(np.radians(45))

    check(Rx * Ry * Rz)
    check(Rz * Ry * Rx)
    check(Rz * Ry )
