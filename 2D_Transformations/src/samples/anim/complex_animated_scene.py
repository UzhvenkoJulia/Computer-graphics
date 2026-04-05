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


if __name__ == '__main__':
    animated_scene = AnimatedSceneSample(
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


    def finish_rotation(scene):
        print("Finished rotation")


    def finish_scale(scene):
        print("Finished scale animation")


    def finish_translation(scene):
        print("Finished translation")


    translation_animation = TranslationAnimation(
        end=vertex(3, 3),
        channel="rect",
        frames=30,
        animation_listener=finish_translation,
        apply_geometry_transformation_on_finish=True,
    )

    rotation_animation = RotationAnimation(
        end=np.radians(45),
        frames=50,
        channel="rect",
        animation_listener=finish_rotation,
        apply_geometry_transformation_on_finish=True,
    )

    scale_animation = ScaleAnimation(
        end=(2, 2),
        frames=50,
        channel="rect",
        animation_listener=finish_scale,
        apply_geometry_transformation_on_finish=True, )

    animated_scene.add_animations(
        scale_animation,
        rotation_animation,
        translation_animation,
    )

    animated_scene.show()
