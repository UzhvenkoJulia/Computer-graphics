from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

ID = "ID"
ID_ORIG = "ID_ORIG"
rectangle_vertices = [   # Вершини прямокутника
    0.5, 0.5,
    1, 0.5,
    1, 1,
    0.5, 1,
]

class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIG] = Polygon(
            rectangle_vertices,
            linewidth=1.0, color="green"
        )

        self[ID] = Polygon(
            rectangle_vertices,
            linewidth=3.0, color="red"
        )


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-0.5, -0.5, 2.3, 2.3),  # розмірність системи координат
        title="",  # заголовок рисунка
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/05_vector.gif",    # шлях для запису анімації у файл
    )

    T = Mat3x3(
        1, 0, 0.5,
        0, 1, 0.5,
        0, 0, 1
    )

    # T1 = Mat3x3(
    #     1, 0, -0.5,
    #     0, 1, -0.5,
    #     0, 0, 1
    # )

    # T_inv = T.inverse()

    scene.add_animations(
        TrsTransformationAnimation(end=T, channel=ID, apply_geometry_transformation_on_finish=True),
        # TrsTransformationAnimation(end=T_inv, channel=ID),
    )

    scene.show()
