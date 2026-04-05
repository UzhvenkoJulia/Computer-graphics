from src.engine.model.Point import SimplePoint
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

ID_VERTICES = "ID_VERTICES"
ID_CENTER = "Center"
ID = "Vector"


class AnimatedSceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_VERTICES] =  SimplePoint(
            0.5, 0.5,
            1, 0.5,
            1, 1,
            0.5, 1,
            color="green",
            vertex_size=100,
        )

        self[ID] = Polygon(
            0.5, 0.5,
            1, 0.5,
            1, 1,
            0.5, 1,
            linewidth=2.0, color="blue")

        self[ID_CENTER] = SimplePoint(
            0.75, 0.75,
            color="orange",
            vertex_size=100,
        )


def frame1(scene):
    poly: Polygon = scene[ID]
    poly.color = "blue"


def frame2(scene):
    poly: Polygon = scene[ID]
    poly.transformation = Mat3x3.scale(2, 2)
    poly.color = "red"
    poly.linewidth = 3.0

    vert: SimplePoint = scene[ID_VERTICES]
    vert.transformation = Mat3x3.scale(2, 2)

    scene[ID_CENTER].transformation = Mat3x3.scale(2, 2)


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
        # out_file ="img/05_vector.gif",
    )

    scene.add_frames(
        frame1,
        # frame2,
    )

    scene.show()
