from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

rectangle_vertices = [  # Вершини прямокутника
    -2, 0,
    0, 2,
    2, 0,
    0, -2
]


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
        image_size=(8, 8),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-2, -2, 2, 2),  # розмірність системи координат
        title="",  # заголовок рисунка
        # grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
    )

    transf = (
            Mat3x3.translation(0.5, 0.5) *
            Mat3x3.rotation(30, False) *
            Mat3x3.scale(0.5, 0.5)
    )

    transf_1 = transf.inverse()

    complex = TrsTransformationAnimation(end=transf, channel="rect")
    complex2 = TrsTransformationAnimation(end=transf_1, channel="rect")
    identity = TrsTransformationAnimation(end=Mat3x3.identity(), channel="rect")

    scene.add_animations(
        complex,
        identity,
        # complex2,
    )

    scene.show()
