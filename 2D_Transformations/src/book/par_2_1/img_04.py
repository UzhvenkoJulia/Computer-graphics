import numpy as np

from src.base.arrow import draw_vector
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
            P1 = np.array([0.5, 1.3])
            U1 = np.array([1.1, 0.5])
            draw_vector(P1, U1, color="blue",
                        label=r'$v$',
                        label_offset=(-0.15, 0.1),
                        )

            P2 = np.array([1.25, 0.7])
            U2 = -U1

            draw_vector(P2, U2, color="brown", label=r'$-v$',
                        label_offset=(-0.3, 0.10),
                        )

    scene = Scene(
        coordinate_rect=(-1, -1, 3, 3),
        grid_show=False
    )
    scene.add_frames(frame1)
    scene.show()

