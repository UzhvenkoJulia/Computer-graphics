import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3
from src.math.Vec3 import vertex


class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        polygon = Polygon()
        polygon.set_geometry(
            0, 1,
            1, 0,
            2, 1,
            1, 2
        )
        polygon.show_local_frame()
        # polygon.pivot(0, 1)
        polygon.pivot(0.5, 0.5)
        polygon.show_pivot()
        polygon["color"] = "blue"
        polygon["line_style"] = ":"

        self["rect"] = polygon


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-4, -1, 4, 5),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        # grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
    )

    translation = TranslationAnimation(
        end=vertex(3, 3),
        channel="rect",
        frames=100,
        # animation_listener=finish,
    )

    scale = ScaleAnimation(
        end=(1, 3),
        # frames=100,
        channel="rect",
        # animation_listener=rotation
    )

    rotation = RotationAnimation(
        end=np.radians(30),
        # frames=100,
        channel="rect",
        # animation_listener=translation
    )

    transf = (
        # Mat3x3.translation(3, 4) *
            Mat3x3.rotation(30, False) *
            Mat3x3.scale(1, 3)
    )

    transf_1 = transf.inverse()

    complex = TrsTransformationAnimation(end=transf, channel="rect")

    # scene.add_animation(translation)
    # scene.add_animation(rotation)
    # scene.add_animation(scale)

    scene.add_animation(complex)

    scene.show()
