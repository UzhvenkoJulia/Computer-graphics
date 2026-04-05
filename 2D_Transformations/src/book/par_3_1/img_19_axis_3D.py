from src.engine.model.Point import SimplePoint
from src.engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon
from src.math.Mat3x3 import Mat3x3

ID = "ID"
ID_ORIG = "ID_ORIG"
LINE_WIDTH = 3.0

rectangle_vertices = [    # Вершини прямокутника
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

povot_vectex = [
    0.5, 0.5
]

S = Mat3x3.scale(2, 2)
R = Mat3x3.rotation(45, is_radians=False)
T = Mat3x3.translation(-0.5, -0.5)
T_1 = T.inverse()

def frame_1(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.color = "grey"
    poligon.line_style = "--"

    scene["pivot"].transformation = T


def frame_2(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = T
    poligon.color = "grey"
    poligon.line_style = "--"

    scene["pivot"].transformation = T

def frame_3(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = S * T
    poligon.color = "grey"
    poligon.line_style = "--"

    scene["pivot"].transformation = S * T

def frame_4(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = R * S * T

    poligon.color = "grey"
    poligon.line_style = "--"

    # scene["pivot"].transformation = T

def frame_5(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = T.inverse() * R * S * T
    poligon.color = "red"
    poligon.line_style = "-"

    scene["pivot"].transformation = Mat3x3.identity()


class SceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        rect = Polygon(
            rectangle_vertices,
            linewidth=LINE_WIDTH,
            color="red"
        )
        # rect.pivot(0.5, 0.5)
        # rect.show_pivot(True)
        self[ID] = rect

        self["pivot"] = SimplePoint(povot_vectex
                                    , color="red",
                                    vertex_size=200,
                                    )


if __name__ == '__main__':
    scene = SceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-2., -2, 2, 2),  # розмірність системи координат
        title="",  # заголовок рисунка
        grid_show=False,
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/05_vector.gif",    # шлях для запису анімації у файл
    )

    scene.add_frames(
        # frame_1,
        # frame_2,
        # frame_3,
        frame_4,
        frame_5,
    )

    scene.show()
