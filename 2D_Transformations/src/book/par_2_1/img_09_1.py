import numpy as np

from src.base.arrow import draw_vector
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
        # # Початкові точки для першого набору векторів
        P0 = np.array([0, 0])

        a = np.array([1, 0])
        b = np.array([-1, 1])
        c = np.array([-1, 3])

        draw_vector(P0, a, color="blue")
        draw_vector(P0, b, color="brown")
        draw_vector(P0, c, color="green")




    scene = Scene(
        coordinate_rect=(-1, -1, 5, 4),
        grid_show=False
    )

    scene.add_frames(frame1)
    scene.show()
