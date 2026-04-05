import numpy as np

from src.engine.model.Point import SimplePoint
from src.engine.model.Polygon import Polygon
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

ID_VERTICES = "ID_VERTICES"
ID = "Vector"

P = np.array([0.5, 0.5])
P1 = np.array([1, 1.5])
vt = P1 - P
class AnimatedSceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        points =  SimplePoint(
            0.5, 0.5,
            1, 1.5,
            color="green",
            vertex_size=100,
        )
        points.labels = (("$P$", (0, -0.2)),
                         ("$P_1$", (0, 0.1)))
        points.label_fontsize = 30
        self[ID_VERTICES] = points

        vect = VectorModel(
            vt,
            color="blue")
        vect.transformation = Mat3x3.translation(P)
        vect.label = "$v_t$"
        vect.label_offset = (0.1, 0)
        vect.label_fontsize = 30

        self[ID] = vect


def frame1(scene):
    poly: Polygon = scene[ID]
    poly.color = "blue"


def frame2(scene):


    vert: SimplePoint = scene[ID_VERTICES]



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
        # frame1,
        # frame2,
    )

    scene.show()
