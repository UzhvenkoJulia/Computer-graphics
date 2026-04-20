import numpy as np

from src.engine.model.Vector import Vector
from src.engine.scene.Scene import Scene
from src.math.Mat4x4 import Mat4x4

VECT_KEY1 = "vector"
VECT_KEY2 = "vector2"


def frame0(scene):
    pass


def frame1(scene):
    vector1: Vector = scene[VECT_KEY1]

    vector1.color = "red"
    vector1.linestyle = "solid"

    vector2: Vector = scene[VECT_KEY2]

    vector2.color = "green"
    vector2.linestyle = "solid"

    euler_angles1 = (30, 90, 45)
    euler_angles_rad1 = tuple(np.radians(angle) for angle in euler_angles1)
    vector1.transformation = Mat4x4.rotation_euler(*euler_angles_rad1)

    euler_angles2 = (45, 90, 30)
    euler_angles_rad2 = tuple(np.radians(angle) for angle in euler_angles2)
    vector2.transformation = Mat4x4.rotation_euler(*euler_angles_rad2)


class VectorScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vector = Vector(
            0, 0, 0,
            1, 0, 1
        )
        self[VECT_KEY1] = vector
        vector.color = "brown"
        vector.linewidth = 2.0

        vector2 = Vector(
            0, 0, 0,
            1, 0, 1
        )
        self[VECT_KEY2] = vector2
        vector2.color = "yellow"
        vector2.linewidth = 2.0


if __name__ == '__main__':
    FIGURE_KEY = "polygon"

    sceneVector = VectorScene(
        coordinate_rect=(-1, -1, -1, 3, 3, 3),  # coordinate system dimensions
        title="3D coordinate system",  # figure title
        axis_line_style="--",  # coordinate axis line style
    )

    sceneVector.add_frames(frame0, frame1)
    sceneVector.show()
