import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec3 import vertex

FIGURE_KEY = "rect"

class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        polygon = Polygon(  # створюємо полігон з заданою геометрією
            0, 2,
            2, 0,
            4, 2,
            2, 4
        )
        polygon.show_local_frame()  # відмальовувати локальну систему координат
        polygon.set_local_frame_parameters(
            line_style="-.",
            color=("brown", "orange"),
            line_width=1
        )
        polygon.pivot(2, 2)  # задати координати опорної точки
        polygon.show_pivot()  # відмальовувати опорну точку
        polygon["color"] = "blue"  # колір ліній полігону
        polygon["line_style"] = "-"  # стиль ліній полігону

        self[FIGURE_KEY] = polygon  # додати полігон з ключем "rect" на сцену


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(7, 7),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1, -1, 6, 6),  # розмірність системи координат
        title="Animated scene",  # заголовок рисунка
        # grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_width=2.0, # товщина осей координат
        axis_line_style="--",  # стиль ліній осей координат
        keep_aspect_ratio=True,
    )

    translation = TranslationAnimation(  # створюємо анімацію переміщення
        end=vertex(1, 1),  # значення точки у яку треба перемітити
        channel=FIGURE_KEY,  # ідентифікатор фігури до якої має застосовуватися анімація
        frames=20,  # кількість кадрів анімації
    )

    translation2 = TranslationAnimation(
        end=vertex(0, 0),
        channel=FIGURE_KEY,
        frames=20,
    )

    scale_before = ScaleAnimation(
        end=(1.2, 1.2),
        frames=20,
        channel=FIGURE_KEY,
    )

    scale_before2 = ScaleAnimation(
        end=(1, 1),
        frames=20,
        channel=FIGURE_KEY,
    )

    scale = ScaleAnimation(
        end=(1.5, 1.5),
        frames=20,
        channel=FIGURE_KEY,
    )

    scale2 = ScaleAnimation(
        end=(0.5, 0.5),
        frames=20,
        channel=FIGURE_KEY,
    )

    scale3 = ScaleAnimation(
        end=(1, 1),
        frames=20,
        channel=FIGURE_KEY,
    )

    rotation = RotationAnimation(
        end=np.radians(30),
        frames=20,
        channel=FIGURE_KEY,
    )

    rotation2 = RotationAnimation(
        end=np.radians(-30),
        frames=20,
        channel=FIGURE_KEY,
    )

    rotation3 = RotationAnimation(
        end=np.radians(0),
        frames=20,
        channel=FIGURE_KEY,
    )

    # задаємо послідовність анімацій
    scene.add_animation(scale_before)
    scene.add_animation(scale_before2)
    scene.add_animation(scale)
    scene.add_animation(rotation)
    scene.add_animation(translation)
    scene.add_animation(scale2)
    scene.add_animation(translation2)
    scene.add_animation(rotation2)
    scene.add_animation(scale3)
    scene.add_animation(rotation3)
    scene.show()
