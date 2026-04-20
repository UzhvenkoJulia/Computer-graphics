import numpy as np

from src.engine.animation.QuaternionAnimation import QuaternionAnimation
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion

CUBE_KEY = "cube"
CUBE1_KEY = "cube1"
CUBE2_KEY = "cube2"

angle_x = np.radians(30)
angle_y = np.radians(45)
angle_z = np.radians(60)

Rx = Mat4x4.rotation_x(angle_x)
Ry = Mat4x4.rotation_y(angle_y)
Rz = Mat4x4.rotation_z(angle_z)
R_final = Rz * Ry * Rx

qx = Quaternion.rotation_x(angle_x)
qy = Quaternion.rotation_y(angle_y)
qz = Quaternion.rotation_z(angle_z)
q_final = qz * qy * qx

animation_quat_x = QuaternionAnimation(
    end_quaternion=qx,
    channel=CUBE_KEY,
    apply_geometry_transformation_on_finish=True,
)

animation_quat_y = QuaternionAnimation(
    end_quaternion=qy,
    channel=CUBE_KEY,
    apply_geometry_transformation_on_finish=True,
)

animation_quat_z = QuaternionAnimation(
    end_quaternion=qz,
    channel=CUBE_KEY,
    apply_geometry_transformation_on_finish=True,
)

animation_quat_final = QuaternionAnimation(
    end_quaternion=q_final,
    channel=CUBE1_KEY,
    apply_geometry_transformation_on_finish=True,
)


class AnimScene(AnimatedScene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        cube = Cube( alpha=0.1)
        self[CUBE_KEY] = cube
        cube.show_pivot()
        cube.show_local_frame()

        cube = Cube( alpha=0.1,
                    color="grey",
                    edge_color="red", )
        self[CUBE1_KEY] = cube
        cube.show_pivot()
        cube.show_local_frame()

        cube = Cube( alpha=0.1,
                    color="yellow",
                    edge_color="black", )
        self[CUBE2_KEY] = cube
        cube.show_pivot()
        cube.show_local_frame()
        cube.rotation = R_final

if __name__ == '__main__':
    animated_scene = AnimScene()

    animated_scene.add_animations(animation_quat_x,
                                  animation_quat_y,
                                  animation_quat_z)

    animated_scene.add_animation(animation_quat_final)
    animated_scene.show()
