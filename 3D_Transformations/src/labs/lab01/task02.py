import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4
from src.math.utils_matrix import decompose_affine_2

if __name__ == '__main__':
    CUBE_KEY = "cube"
    CUBE_TARGET_KEY = "cube_target"

    class CubeScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            cube = Cube(alpha=0.1)
            self[CUBE_KEY] = cube

            cube_target = Cube(
                               alpha=0.1, color="grey",
                               line_width=0.5, line_style="-.")
            self[CUBE_TARGET_KEY] = cube_target

    animated_scene = CubeScene()

    OX = Vec4(1, 0, 0)
    OY = Vec4(0, 1, 0)
    OZ = Vec4(0, 0, 1)

    angle_x, angle_y, angle_z = np.radians(30), np.radians(45), np.radians(60)

    Rx = Mat4x4.rotation_x(angle_x)
    Ry = Mat4x4.rotation_y(angle_y)
    Rz = Mat4x4.rotation_z(angle_z)

    R_final = Rz * Ry * Rx

    # R1 = Mat4x4.rotation_x(45, is_radians=False)
    # R2 = Mat4x4.rotation_z(19, is_radians=False)
    # R3 = Mat4x4.rotation_y(33, is_radians=False)
    # R_final = R3 * R2* R1* Rz * Ry * Rx

    T1, R1, S1, u, theta = decompose_affine_2(R_final)

    animation_1 = RotationAnimation(
        end=theta,
        axis=u,
        channel=CUBE_KEY,
    )

    animation = TrsTransformationAnimation(
        end=R_final,
        channel=CUBE_TARGET_KEY,
    )

    animated_scene.add_animations(
        animation_1,
        animation,
    )

    animated_scene.show()
