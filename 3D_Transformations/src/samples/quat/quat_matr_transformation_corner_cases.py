import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.samples.quat.quat_matr_transformation import check

if __name__ == '__main__':

    Rx = Mat4x4.rotation_x(np.radians(190))
    Ry = Mat4x4.rotation_y(np.radians(190))
    Rz = Mat4x4.rotation_z(np.radians(190))

    check(Rx)
    check(Ry)
    check(Rz)

    check(Rx * Ry)
