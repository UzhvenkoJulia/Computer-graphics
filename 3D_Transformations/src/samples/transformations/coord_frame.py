import numpy as np

from src.engine.model.CoordinateFrame import CoordinateFrame
from src.engine.scene.Scene import Scene
from src.math.Mat4x4 import Mat4x4

if __name__ == '__main__':
    RECT_KEY = "rect"


    class CoordinateFrameScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            coord_frame = CoordinateFrame()
            self[RECT_KEY] = coord_frame


    ############## Frame 1 ##################
    def frame1(scene: Scene):
        rect: CoordinateFrame = scene[RECT_KEY]
        rect.line_style = "--"  # line style


    ##############################################
    ##############################################

    Rz = Mat4x4.rotation_z(np.radians(45))
    Rx = Mat4x4.rotation_x(np.radians(15))
    S = Mat4x4.scale(1)
    T = Mat4x4.translation(0, 0, 0)


    ############## Frame 2 ##################
    def frame2(scene: Scene):
        rect: CoordinateFrame = scene[RECT_KEY]

        # rect.show_local_frame()

        R = Rz

        rect.alpha = 1.0
        rect.transformation = T * R * S


    ############## Frame 3 ##################
    def frame3(scene: Scene):
        rect: CoordinateFrame = scene[RECT_KEY]

        R = Rx * Rz

        rect.transformation = T * R * S


    simple_scene = CoordinateFrameScene(
        axis_color="grey",  # coordinate axis color
    )

    simple_scene.add_frames(
        frame1,
        frame2,
        frame3,
    )  # add frames to the scene

    simple_scene.show()
