import numpy as np

from src.base.arrow import draw_vector
from src.base.points import draw_point
from src.base.text import print_label
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
        # Координати точок
        P1 = np.array([0, 0])
        P2 = np.array([-1.5, 1])
        P3 = np.array([2, 2])

        # Вектори
        v2 = P2 - P1
        v3 = P3 - P1

        draw_vector(P1, v2, color="blue")
        draw_vector(P1, v3, color="brown")

        a2 = 0.5
        a3 = 0.6
        a2v2 = a2 * v2
        a3v3 = a3 * v3

        draw_vector(P1, a2v2, color="blue", )
        draw_vector(P1, a3v3, color="brown")

        draw_vector(P1 + a2v2, a3v3, color="brown", )
        draw_vector(P1 + a3v3, a2v2, color="blue")

        P = P1 + a2v2 + a3v3
        draw_point(P, label=r"$P$",
                   label_offset=(-0.3, 0.1),
                   size=30,
                   color="red"
                   )

        print_label(P1,
                    # label_color="green",
                    label=r"$P_1$",
                    label_offset=(-0.3, -0.7)
                    )

        print_label(P2,
                    # label_color="green",
                    label=r"$P_2$",
                    label_offset=(-0.5, 0.2)
                    )

        print_label(P3,
                    # label_color="green",
                    label=r"$P_3$",
                    label_offset=(-0.3, 0.2)
                    )


    scene = Scene(
        coordinate_rect=(-3, -1, 3, 4),
        grid_show=False
    )
    scene.add_frames(frame1)
    scene.show()
