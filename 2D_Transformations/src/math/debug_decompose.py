from src.math.Mat3x3 import Mat3x3
from src.math.utils_matrix import decompose_affine3

if __name__ == '__main__':
    transf = Mat3x3.translation(3, 4) * Mat3x3.rotation(33, False) * Mat3x3.scale(2, 3)

    print(transf)

    translation, angle, scales = decompose_affine3(transf)

    print(translation)
    print(angle)
    print(scales)

    print()

    T = Mat3x3.translation(*translation)
    R = Mat3x3.rotation(angle)
    S = Mat3x3.scale(*scales)

    transformation = T * R * S

    print(transformation)
