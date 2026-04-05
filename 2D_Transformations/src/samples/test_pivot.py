import numpy as np

from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

FIGURE_KEY = "polygon"


class SampleScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        triangle = Polygon(
            0, 0,
            2, 0,
            1, 1,
        )

        self[FIGURE_KEY] = triangle

        triangle.pivot(1, 0)
        triangle.show_pivot()
        triangle.show_local_frame()


def frame1(scene):
    triangle = scene[FIGURE_KEY]
    # Задаємо параметри полігону
    # triangle["show_frames"] = True
    triangle["color"] = "blue"  # колір ліній
    triangle["line_style"] = "--"  # стиль ліній


def frame2(scene):
    triangle = scene[FIGURE_KEY]
    # задаємо трансформацію
    # triangle.scale(2, 1)          # масштабування
    triangle.rotation = np.radians(30)  # поворот
    # triangle.translation(2, 1)    # перенесення
    triangle["line_style"] = "-"  # стиль ліній
    # малюємо полігон


scene = SampleScene(
    image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
    coordinate_rect=(-1, -1, 3, 3),  # розмірність системи координат
    title="Picture",  # заголовок рисунка
    grid_show=False,  # чи показувати координатну сітку
    base_axis_show=False,  # чи показувати базові осі зображення
    axis_show=True,  # чи показувати осі координат
    axis_color=("red", "green"),  # колір осей координат
    axis_line_style="-."  # стиль ліній осей координат
)
scene.add_frames(frame1, frame2)
scene.show()
