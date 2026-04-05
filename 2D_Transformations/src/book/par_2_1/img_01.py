import numpy as np

from src.base.arrow import draw_vector
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
        U = np.array((1, 1))
        P1 = np.array((0, 0))
        P2 = np.array((0.5, 1))
        P3 = np.array((0, 1.4))

        draw_vector(P1, U, color="blue")
        draw_vector(P2, U, color="blue")
        draw_vector(P3, U, color="blue")


    scene = Scene(
        coordinate_rect=(-1, -1, 3, 5),
        grid_show=False
    )
    scene.add_frames(frame1)
    scene.show()
