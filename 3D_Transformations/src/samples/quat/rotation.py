import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.math.utils_matrix import decompose_translation_quaternion_scale

if __name__ == '__main__':
    angle_x = np.radians(30)
    angle_y = np.radians(45)
    angle_z = np.radians(60)

    Rx = Mat4x4.rotation_x(angle_x)
    Ry = Mat4x4.rotation_y(angle_y)
    Rz = Mat4x4.rotation_z(angle_z)
    R = Rz * Ry * Rx


    qx = Quaternion.rotation_x(angle_x)
    qy = Quaternion.rotation_y(angle_y)
    qz = Quaternion.rotation_z(angle_z)
    q = qz * qy * qx
    Rq = q.toRotationMatrix()

    T, quat_from_R, S = decompose_translation_quaternion_scale(R)
    print(f"{q=}")
    print(f"{quat_from_R=}")
    print(f"{quat_from_R - q=}")


    print(f"{R=}")
    print("------------")
    print(f"{Rq=}")
    print("------------")

    print(f"{R - Rq=}")



