import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY = "rect"
    RECT_2_KEY = "rect_2"
    VECT_KEY = "vector"
    O = vertex(0, 0, 0)
    t1 = Vec4(1, 0, 0)
    t2 = Vec4(1, 1, 0)
    t3 = Vec4(0, 1, 0)
    ax = Vec4(0.557, 0.500, 0.663).normalized()


    class SimplePolygonScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            polygon = SimplePolygon(
                                    O,
                                    O + t1,
                                    O + t2,
                                    O + t3,
                                    edgecolor="red",
                                    color="blue",
                                    alpha=0.2
                                    )
            self[RECT_KEY] = polygon
            polygon.show_local_frame()

            polygon2 = SimplePolygon(
                                     O,
                                     O + t1,
                                     O + t2,
                                     O + t3,
                                     edgecolor="black",
                                     color="blue",
                                     alpha=0.2,
                                     )
            self[RECT_2_KEY] = polygon2
            polygon2.show_local_frame()

            self[VECT_KEY] = Vector(
                O,
                O + ax,
                color="brown"
            )


    animated_scene = SimplePolygonScene(
        coordinate_rect=(-1, -1, -1, 2, 2, 2),  # coordinate system dimensionsps
    )

    frames_num = 60

    angle = np.radians(45)
    translation_vector = Vec3(1, 1, 1)
    scales = Vec3(2, 2, 2)

    T = Mat4x4.translation(translation_vector)
    R = Mat4x4.rotation(angle, ax)
    S = Mat4x4.scale(scales)
    R_final = T * R * S

    animation_rotation = RotationAnimation(
        end=angle,
        axis=ax,
        frames=frames_num,
        channel=RECT_KEY,
    )

    animation_trans = TranslationAnimation(
        translation_vector,
        frames=frames_num,
        channel=RECT_KEY,
    )

    animation_scale = ScaleAnimation(
        scales,
        frames=frames_num,
        channel=RECT_KEY,
    )

    common_animation = TrsTransformationAnimation(
        end=R_final,
        frames=frames_num,
        interval=5,
        channel=RECT_2_KEY,
    )

    animated_scene.add_animation(animation_scale)
    animated_scene.add_animation(animation_rotation)
    animated_scene.add_animation(animation_trans)

    animated_scene.add_animation(common_animation)
    animated_scene.show()
