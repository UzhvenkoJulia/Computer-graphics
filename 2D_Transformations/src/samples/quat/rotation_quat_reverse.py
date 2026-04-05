import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.math.utils_matrix import is_same_matrix

if __name__ == '__main__':


    angle, axis = np.radians(30), Vec3(1, 2, 3).normalized()

    m_rot = Mat4x4.rotation(angle, axis)

    q = Quaternion.rotation(angle, axis)
    m_rot_from_q = q.toRotationMatrix()

    print(m_rot)

    print(f"Matrix is the same: {is_same_matrix(m_rot, m_rot_from_q)}")

    angle_restored_quat, axis_restored_quat = q.to_angle_axis()
    print(f"rotation quaternion: {q}")

    # angle_restored_matr, axis_restored_matr = rotation_matrix_to_axis_angle(m_rot)
    angle_restored_matr, axis_restored_matr = m_rot.to_angle_axis()

    print("Original       : ", angle, axis)
    print("Restored (quat): ", angle_restored_quat, axis_restored_quat)
    print("Restored (matr): ", angle_restored_matr, axis_restored_matr)





