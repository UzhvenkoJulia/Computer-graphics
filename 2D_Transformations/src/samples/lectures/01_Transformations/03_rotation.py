import numpy as np

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene

rectangle_vertices = (  # Вершини прямокутника
    -2, 0,
    0, 2,
    2, 0,
    0, -2
)


class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        polygon = Polygon(rectangle_vertices)
        polygon.show_local_frame()
        polygon.show_pivot()
        polygon["color"] = "blue"
        polygon["line_style"] = ":"
        self["rect"] = polygon


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-2, -2, 4, 5),  # розмірність системи координат
        title="",  # заголовок рисунка
        # grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/animation_rotation.gif",    # шлях для запису анімації у файл
    )

    rotation = RotationAnimation(
        end=np.radians(70),
        # frames=100,
        channel="rect",
    )

    scene.add_animation(rotation)
    scene.show()
