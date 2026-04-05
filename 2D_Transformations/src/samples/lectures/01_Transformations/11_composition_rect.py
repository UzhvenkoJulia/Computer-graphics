import numpy as np

from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

ID_SEQUENCE = "ID"
ID_COMPOSITION = "ID_ORIG"
rectangle_vertices = [   # Вершини прямокутника
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self[ID_SEQUENCE] = Polygon(
            rectangle_vertices,
            linewidth=3.0, color="blue"
        )

        self[ID_COMPOSITION] = Polygon(
            rectangle_vertices,
            linewidth=3.0,
            color="red"
        )



if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1.5, -0.5, 2.2, 3.5),  # розмірність системи координат
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

    R = Mat3x3(   # поворот на кут phi=45 градусів.
        cos_phi, -sin_phi,   0,
        sin_phi,  cos_phi,   0,
              0,        0,   1
    )

    T = Mat3x3(  # перенос на вектор (0.5, 0.5)
        1, 0, 0.5,
        0, 1, 0.5,
        0, 0,   1
    )

    M = T * R * S

    scene.add_animations(
        TrsTransformationAnimation(end=S, channel=ID_SEQUENCE, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=R, channel=ID_SEQUENCE, apply_geometry_transformation_on_finish=True),
        TrsTransformationAnimation(end=T, channel=ID_SEQUENCE, apply_geometry_transformation_on_finish=True),
        # TrsTransformationAnimation(end=M, channel=ID_COMPOSITION, apply_geometry_transformation_on_finish=True),
    )

    scene.show()
