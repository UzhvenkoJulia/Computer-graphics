import numpy as np

from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

ID_RECT = "ID_RECT"
ID_RECT2 = "ID_RECT2"
ID_RECT_ORIG = "ID_RECT_ORIG"
ID_PIVOT = "ID_PIVOT"
rectangle_vertices = [  # Вершини прямокутника
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]
pivot_vectex = [
    0.5, 0.5
]


class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        rect_orig = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            line_style="--",
            color="grey",
        )
        rect_orig.show_pivot(True)
        rect_orig.pivot(0.5, 0.5)
        self[ID_RECT_ORIG] = rect_orig

        rect = Polygon(
            rectangle_vertices,
            linewidth=3.0, color="blue",
        )
        rect["labels"] = (0.5, 0.5)
        self[ID_RECT] = rect

        rect2 = Polygon(
            rectangle_vertices,
            linewidth=3.0, color="red",
        )
        # rect2.pivot(0.5, 0.5)
        # rect2.show_pivot(True)
        self[ID_RECT2] = rect2


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1.5, -1.5, 2, 2),  # розмірність системи координат
        title="",  # заголовок рисунка
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/05_vector.gif",    # шлях для запису анімації у файл
    )

    S = Mat3x3(  # рівномірний розтяг в 2 рази
        2, 0, 0,
        0, 2, 0,
        0, 0, 1,
    )

    phi = np.deg2rad(45)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    R = Mat3x3(  # поворот на кут phi=45 градусів.
        cos_phi, -sin_phi, 0,
        sin_phi, cos_phi, 0,
        0, 0, 1
    )

    T = Mat3x3(  # перенос на вектор (-0.5, -0.5)
        1, 0, -pivot_vectex[0],
        0, 1, -pivot_vectex[1],
        0, 0, 1
    )

    scene.add_animations(

        TrsTransformationAnimation(end=T, channel=ID_RECT, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=S, channel=ID_RECT, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=R, channel=ID_RECT, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=T.inverse(), channel=ID_RECT, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=T.inverse() * R * S * T, channel=ID_RECT2, apply_geometry_transformation_on_finish=True),
        # TrsTransformationAnimation(end= R * S, channel=ID_RECT2, apply_geometry_transformation_on_finish=True),
    )

    scene.show()
