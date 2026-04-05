import numpy as np

from src.base.arc import draw_arc
from src.base.text import print_label
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene

ID_VERTICES = "ID_VERTICES"
ID_CENTER = "Center"
ID = "Vector"

LABEL_FONT_SIZE = 30
r = 2
O = np.array([0, 0])
ox = np.array([1, 0]) * r
phi = np.deg2rad(30)
cos_phi = np.cos(phi)
sin_phi = np.sin(phi)

theta = np.deg2rad(60)
cos_theta = np.cos(theta)
sin_theta = np.sin(theta)

v0 = np.array([r * cos_phi, r * sin_phi])  # Перший вектор
v1 = np.array([r * cos_theta, r * sin_theta])  # Другий вектор


class AnimatedSceneSample(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vect0 = VectorModel(v0)
        self["v0"] = vect0
        vect0["color"] = "blue"
        vect0["label"] = "$r$"
        vect0["label_offset"] = (0.3, 0.3)
        vect0["label_fontsize"] = LABEL_FONT_SIZE

        vect1 = VectorModel(v1)
        self["v1"] = vect1
        vect1["color"] = "red"
        vect1["label"] = "$r$"
        vect1["label_offset"] = (0.1, 0.5)
        vect1["label_fontsize"] = LABEL_FONT_SIZE


def frame1(scene: Scene):
    draw_arc(O, ox, v0,
             radius=0.45,
             color="blue",
             linestyle="--",
             linewidth=2.0,
             )

    draw_arc(O, v0, v1,
             radius=0.6,
             color="red",
             linestyle="--",
             linewidth=2.0,
             )

    print_label(start=(ox + v0) * 0.13,
                label=r"$\theta$",
                label_offset=(0.0, -0.05),
                label_fontsize=LABEL_FONT_SIZE,
                )

    print_label(start=(v0 + v1) * 0.18,
                label=r"$\varphi$",
                # label_offset=(-0.2, 0),
                label_fontsize=LABEL_FONT_SIZE
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
        # out_file ="img/05_vector.gif",
    )

    scene.add_frames(
        frame1,
    )
    scene.show()
