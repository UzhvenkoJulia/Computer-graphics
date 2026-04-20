import numpy as np

from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.model.Vector import Vector
from src.engine.scene.Scene import Scene
from src.math.Mat4x4 import Mat4x4

if __name__ == '__main__':
    RECT_KEY = "rect"
    VECT_KEY = "vector"


    class SimplePolygonScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self[RECT_KEY] = SimplePolygon(
                                           1, 0, 0,
                                           1, 1, 0,
                                           1, 1, 1,
                                           1, 0, 1,
                                           edgecolor="red",
                                           )

            self[VECT_KEY] = Vector(
                                    1, 1, 0,
                                    2, 1, 0.8,
                                    color="brown"
                                    )


    # Rz = Mat4x4.rotation_z(np.radians(45))
    # Ry = Mat4x4.rotation_y(np.radians(30))
    # Rx = Mat4x4.rotation_x(np.radians(15))
    # T = Mat4x4.translation(1, 0, 0)
    # T = Mat4x4.translation(0.557, 0.500, 0.663,)
    T = Mat4x4.translation(1, 1, 0, )
    T1 = T.inverse()


    ############## Frame 1 ##################
    def frame1(scene: Scene):
        rect: SimplePolygon = scene[RECT_KEY]

        # rect.color = "blue"  # line color
        rect.alpha = 0.2


    ############## Frame 2 ##################
    def frame2(scene: Scene):
        rect: SimplePolygon = scene[RECT_KEY]
        vect: Vector = scene[VECT_KEY]

        u = (vect.transformed_geometry[1] - vect.transformed_geometry[0]).xyz
        ux, uy, uz = u
        print(*u)

        R1 = Mat4x4.rotation(np.radians(-20), u)
        R = T * R1 * T1

        rect.color = "blue"  # line color
        rect.transformation = R


    ############## Frame 3 ##################
    def frame3(scene: Scene):
        rect: SimplePolygon = scene[RECT_KEY]
        vect: Vector = scene[VECT_KEY]

        u = (vect.transformed_geometry[1] - vect.transformed_geometry[0]).xyz
        ux, uy, uz = u
        print(*u)

        R1 = Mat4x4.rotation(np.radians(90), u)
        R = T * R1 * T1

        rect.color = "blue"  # line color
        rect.transformation = R


    ############## Frame 4 ##################
    def frame4(scene: Scene):
        rect: SimplePolygon = scene[RECT_KEY]
        vect: Vector = scene[VECT_KEY]

        u = (vect.transformed_geometry[1] - vect.transformed_geometry[0]).xyz
        ux, uy, uz = u
        print(*u)

        R1 = Mat4x4.rotation(np.radians(180), u)
        R = T * R1 * T1

        rect.color = "blue"  # line color
        rect.transformation = R


    ############## Frame 5 ##################
    def frame5(scene: Scene):
        rect: SimplePolygon = scene[RECT_KEY]
        vect: Vector = scene[VECT_KEY]

        u = (vect.transformed_geometry[1] - vect.transformed_geometry[0]).xyz
        ux, uy, uz = u
        print(*u)

        R1 = Mat4x4.rotation(np.radians(230), u)
        R = T * R1 * T1

        rect.color = "blue"  # line color
        rect.transformation = R


    simple_scene = SimplePolygonScene(
        coordinate_rect=(0, 0, 0, 2, 2, 2)
    )

    simple_scene.add_frames(
        frame1,
        frame2,
        frame3,
        frame4,
        frame5,
    )  # add frames to the scene

    simple_scene.show()
