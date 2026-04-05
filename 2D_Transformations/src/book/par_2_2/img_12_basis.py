import numpy as np

from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene

FIGURE_E_1 = "$a$"
FIGURE_E_2 = "$b$"
FIGURE_E_3 = "$c$"
# FIGURE_E_1 = "$e_1$"
# FIGURE_E_2 = "$e_2$"
# FIGURE_E_3 = "$e_3$"
if __name__ == '__main__':

    class LineScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            P = np.array([2, 1])
            Q = np.array([3.5, 2.5])
            R = np.array([1.2, 1.5])

            E1 = Q-P
            E2 = R-P

            E3 = E1 * 1.5 + E2 * 1.3

            e1 = VectorModel(E1)
            e1["color"] = "blue"
            e1["label"] = FIGURE_E_1
            e1["label_offset"] = -0., -0.4
            e1["label_fontsize"] = 28
            e1.translation = P
            self[FIGURE_E_1] = e1

            e2 = VectorModel(E2)
            e2["color"] = "red"
            e2["label"] = FIGURE_E_2
            e2["label_offset"] = -0.3, -0.3
            e2["label_fontsize"] = 28
            e2.translation = P
            self[FIGURE_E_2] = e2

            e3 = VectorModel(E3)
            e3["color"] = "green"
            e3["label"] = FIGURE_E_3
            e3["label_offset"] = -0.3, -0.
            e3["label_fontsize"] = 28
            e3.translation = P
            self[FIGURE_E_3] = e3








    sample_scene = LineScene(
        coordinate_rect=(-1, -1, 5, 5),
        grid_show=False,
        axis_show=True
    )

    sample_scene.show()

