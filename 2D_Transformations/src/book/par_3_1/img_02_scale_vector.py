from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

ID_ORIG = "Vector_Orig"
ID = "Vector"


class AnimatedSceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vector = VectorModel(1, 0.5)
        vector["color"] = "blue"
        self[ID] = vector


def frame1(scene):
    vect: VectorModel = scene[ID]
    vect.color = "grey"


def frame2(scene):
    vect: VectorModel = scene[ID]
    vect.transformation = Mat3x3.scale(2, 3)
    vect.color = "blue"


if __name__ == '__main__':
    scene = AnimatedSceneSample(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-0.5, -0.5, 2.3, 2),  # розмірність системи координат
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
        frame2,
    )

    scene.show()
