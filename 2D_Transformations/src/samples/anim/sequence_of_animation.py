import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec3 import vertex


class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self["rect"] = Polygon(
            0, 0,
            1, 0,
            1, 1,
            0, 1
        )

        self["rect"].color = "blue"
        self["rect"].line_style = "-"

        self["rect"].show_local_frame()
        self["rect"].show_pivot()


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-3, -1, 6, 6),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
    )

    translation = TranslationAnimation(
        end=vertex(1, 1),
        channel="rect",
        frames=30,
        # apply_geometry_transformation_on_finish=True,
        # animation_listener=finish,
    )

    scale = ScaleAnimation(
        end=(2, 3),
        frames=50,
        channel="rect",
        apply_geometry_transformation_on_finish=True,
        # animation_listener=rotation
    )

    rotation = RotationAnimation(
        end=np.radians(45),
        frames=50,
        channel="rect",
        apply_geometry_transformation_on_finish=True,
        # animation_listener=translation
    )

    scene.add_animation(translation)
    scene.add_animation(rotation)
    scene.add_animation(scale)
    scene.show()
