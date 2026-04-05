import numpy as np

from src.base.text import print_label
from src.engine.model.Point import SimplePoint
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene

O = np.array([0, 0])
x = np.array([3.5, 0])  # Перший вектор
y = np.array([0, 2.5])  # Другий вектор
c = 2 * x + 0.5 * y

RECT_KEY = "coord_frame"
if __name__ == '__main__':
    ############## Frame 1 ##################
    def frame1(scene: Scene):

        print_label(start=(3.9, 0),
                    label=r"$x$",
                    label_offset=(-0.1, 0.1)
                    )

        print_label(start=(0, 2.8),
                    label=r"$y$",
                    label_offset=(-0.2, 0)
                    )

    simple_scene = Scene(
        coordinate_rect=(-1, -1, 4, 3),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
    )

    P = (2., 1.2)

    v_x = VectorModel(P)
    v_x["color"] = "blue"
    v_x["label"] = "$v$"
    v_x["label_offset"] = (-0.2,0)
    simple_scene["r"] = v_x

    point = SimplePoint(P)
    point["color"] = "red"
    point["labels"] = (
        ("$P$", (-0.05, 0.15)),
    )
    simple_scene["point"] = point

    orig = SimplePoint((0,0))
    orig["color"] = "red"
    orig["labels"] = (
        ("$O$", (-0.25, -0.3)),
    )
    simple_scene["orig"] = orig

    p = SimplePoint((1, 0), (2, 0), (3, 0))
    p["labels"] = (
        ("$1$", (-0.05, -0.35)),
        ("$2$", (-0.05, -0.35)),
        ("$3$", (-0.05, -0.35)),
    )
    p["label_fontsize"] = 18
    simple_scene["grade_x"] = p

    py = SimplePoint((0, 1), (0, 2))
    py["labels"] = (
        ("$1$", (-0.25, -0.1)),
        ("$2$", (-0.25, -0.1)),
    )
    py["label_fontsize"] = 18
    simple_scene["grade_y"] = py

    simple_scene.add_frames(
        frame1,
    )

    simple_scene.show()

