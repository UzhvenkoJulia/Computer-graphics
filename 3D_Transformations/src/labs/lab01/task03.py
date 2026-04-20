import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4

if __name__ == '__main__':
    CUBE_KEY = "cube"
    CUBE_TARGET_KEY = "cube_targer"
    frames_num = 80


    class CubeScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            cube = Cube(alpha=0.1)
            self[CUBE_KEY] = cube
            # cube.show_pivot()
            cube.show_local_frame()

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

    ##### Rx ######
    Y1 = Rx * OY
    Z1 = Rx * OZ

    ##### Ry ######
    # Z2 = Ry * Z1  # this was the bug!!
    Ry_intrinsic = Mat4x4.rotation(angle_y, Y1)  # Rotation around the updated Y1!
    Z2 = Ry_intrinsic * Z1

    animation_x = RotationAnimation(
        end=angle_x,
        axis=OX,
        channel=CUBE_KEY,
    )

    animation_y = RotationAnimation(
        end=angle_y,
        axis=Y1,
        channel=CUBE_KEY,
    )

    animation_z = RotationAnimation(
        end=angle_z,
        axis=Z2,
        channel=CUBE_KEY,
    )

    # R_final = Rz * Ry * Rx  # extrinsic rotation
    R_final = Rx * Ry * Rz    # intrinsic rotation
    animation = TrsTransformationAnimation(
        end=R_final,
        channel=CUBE_TARGET_KEY,
    )

    animated_scene.add_animations(
        animation_x,
        animation_y,
        animation_z,
        animation,
    )

    animated_scene.show()
