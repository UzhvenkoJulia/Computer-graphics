from src.engine.model.VectorModel import VectorModel
from src.engine.animation.TrsTransformationAnimation import TrsTransformationAnimation
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat3x3 import Mat3x3

ID_ORIG = "Vector_Orig"
ID = "Vector"
v = [1, 0.5]    # Початкові координати вектора

class AnimatedSceneSample(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vector_orig = VectorModel(v)
        vector_orig["color"] = "grey"
        self[ID_ORIG] = vector_orig

        vector = VectorModel(v)
        vector["color"] = "blue"
        self[ID] = vector


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
        # out_file ="img/05_vector.gif",  # шлях для запису анімації у файл
    )

    S = Mat3x3(
        2, 0,
        0, 3
    )

    scale = TrsTransformationAnimation(end=S, channel=ID) # to animate transformation
    scene.add_animation(scale)

    scene.show()
