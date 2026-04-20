import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY = "rect"
    VECT_KEY = "vector"
    ax = Vec4(0.557, 0.500, 0.663)
    O = vertex(0, 0, 0)
    t = vertex(0, 1, 0)


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
            # polygon.show_local_frame()

            vector = Vector(
                O,
                O + ax,
            )
            self[VECT_KEY] = vector
            vector.color = "brown"


    animated_scene = SimplePolygonScene(
        coordinate_rect=(-1, -1, -1, 2, 2, 2),  # coordinate system dimensions
    )

    frames_num = 180
    animation = RotationAnimation(
        end=np.radians(90),
        axis=ax,
        frames=frames_num,
        channel=RECT_KEY,
    )

    animated_scene.add_animation(animation)
    animated_scene.show()

