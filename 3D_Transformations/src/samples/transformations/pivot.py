import numpy as np

from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene
from src.math.Mat4x4 import Mat4x4

TRIANGLE_KEY = "rect"
if __name__ == '__main__':
    class SampleScene(Scene):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            triangle = SimplePolygon(
                                     0, 1, 0,
                                     2, 1, 0,
                                     1, 2, 0,
                                     color="grey"
                                     )

            self[TRIANGLE_KEY] = triangle
            triangle.pivot(1, 0, 0)
            triangle.show_pivot()
            triangle.show_local_frame()


    def frame1(scene):
        scene[TRIANGLE_KEY].transformation = Mat4x4.rotation_z(np.radians(30))  # rotation

    scene = SampleScene(
        coordinate_rect=(-1, -1, -1, 3, 3, 3),  # coordinate system dimensions
    )
    scene.add_frames(frame1)
    scene.show()
