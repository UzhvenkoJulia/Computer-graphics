import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY = "rect"
    RECT_KEY1 = "rect1"
    ax = Vec4(0.557, 0.500, 0.663).normalized()
    O = vertex(0, 0, 0)
    t = vertex(0, 1, 0)
    angle_rot = np.radians(23)


    class SimplePolygonScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            polygon = SimplePolygon(
                                    O,
                                    O + ax,
                                    O + t,
                                    edgecolor="red",
                                    )
            self[RECT_KEY] = polygon
            polygon.show_local_frame()

            polygon = SimplePolygon(
                                    O,
                                    O + ax,
                                    O + t,
                                    edgecolor="red",
                                    )
            self[RECT_KEY1] = polygon
            polygon.show_local_frame()


    animated_scene = SimplePolygonScene(
        coordinate_rect=(-1, -1, -1, 3, 3, 3),  # coordinate system dimensionsps
    )

    transformation_matrix = (
            Mat4x4.translation(1, 1, 1) *
            Mat4x4.rotation(angle_rot, ax)
        # * Mat4x4.scale(2,
        #                2,
        #                2)
    )

    frames_num = 60
    animation = TrsTransformationAnimation(
        end=transformation_matrix,
        frames=frames_num,
        interval=5,
        channel=RECT_KEY,
    )

    animation_ax = RotationAnimation(
        end=angle_rot,
        axis=ax,
        frames=frames_num,
        channel=RECT_KEY1,
    )

    animated_scene.add_animation(animation_ax)
    animated_scene.add_animation(animation)
    animated_scene.show()
