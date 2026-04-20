import numpy as np

from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY = "rect"
    RECT_0_KEY = "rect_0"
    VECT_KEY = "vector"
    O = vertex(0, 0, 0)
    t1 = Vec4(1, 0, 0)
    t2 = Vec4(1, 1, 0)

    angle_x = 35
    angle_y = 53
    angle_z = 90

    Rx = Mat4x4.rotation_x(angle_x, False)
    Ry = Mat4x4.rotation_y(angle_y, False)
    Rz = Mat4x4.rotation_z(angle_z, False)

    R_final = Rx * Ry * Rz

    X = Vec4(1, 0, 0)
    Y = Vec4(0, 1, 0)
    Z = Vec4(0, 0, 1)


    def frame1(scene):
        polygon = scene[RECT_KEY]
        y1 = Rx * Y
        z1 = Rx * Z
        rot_y = Mat4x4.rotation(np.radians(angle_y), y1)

        rot = rot_y * Rx

        z2 = rot_y * z1
        rot_z = Mat4x4.rotation(np.radians(angle_z), z2)

        rot = rot_z * rot

        polygon.transformation = rot


    class SimplePolygonScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            polygon = SimplePolygon(
                                    *O.xyz,
                                    *(O + t1).xyz,
                                    *(O + t2).xyz,
                                    edgecolor="red",
                                    )
            self[RECT_KEY] = polygon
            polygon.show_local_frame()

            polygon0 = SimplePolygon(
                                     *O.xyz,
                                     *(O + t1).xyz,
                                     *(O + t2).xyz,
                                     edgecolor="red",
                                     )
            self[RECT_0_KEY] = polygon0
            polygon0.transformation = R_final
            polygon0.alpha = 0.2
            polygon0.color = "green"

            polygon0.show_local_frame()


    simple_scene = SimplePolygonScene(
        axis_color=("#f00000", "#00f000", "#000088"),  # coordinate axis color
        axis_line_width=0.5,
        axis_line_style="-."  # coordinate axis line style
    )

    simple_scene.add_frames(
        frame1,
        # frame2,
        # frame3,
        # frame4,
        # frame5,
        # frame6,
    )  # add frames to the scene

    simple_scene.add_frames(frame1)
    simple_scene.show()
