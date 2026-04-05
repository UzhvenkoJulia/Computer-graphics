import numpy as np

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

phi = np.deg2rad(45)
cos_phi = np.cos(phi)
sin_phi = np.sin(phi)

R = Mat3x3(
    cos_phi, -sin_phi,
    sin_phi, cos_phi
)

T = Mat3x3.translation(1, 1)

RT = R * T
TR = T * R

def frame_R(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = R
    poligon.color = "green"
    poligon.line_style = "--"

def frame_T(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = T
    poligon.color = "green"
    poligon.line_style = "--"

def frame_TR(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = TR
    poligon.color = "red"
    poligon.line_style = "-"

def frame_RT(scene: Scene):
    poligon: Polygon = scene[ID]
    poligon.transformation = RT
    poligon.color = "red"
    poligon.line_style = "-"

class SceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self[ID_ORIG] = Polygon(
            rectangle_vertices,
            linewidth=LINE_WIDTH,
            line_style="--",
            color="grey"
        )

        self[ID] = Polygon(
            rectangle_vertices,
            linewidth=LINE_WIDTH, color="red"
        )


if __name__ == '__main__':
    scene = SceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1., -.5, 2, 3.5),  # розмірність системи координат
        title="",  # заголовок рисунка
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-.",  # стиль ліній осей координат
        keep_aspect_ratio=True,
        # out_file ="img/05_vector.gif",    # шлях для запису анімації у файл
    )

    scene.add_frames(
        frame_R,
        frame_TR,
    )

    scene.show()
