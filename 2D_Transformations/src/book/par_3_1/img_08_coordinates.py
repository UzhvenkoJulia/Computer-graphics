import numpy as np

from src.base.arc import draw_arc
from src.base.text import print_label
from src.engine.model.LineModel import LineModel
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3
from src.math.Vec3 import Vec3

ID = "rect"
LABEL_FONT_SIZE = 26
if __name__ == '__main__':
    O = np.array([0, 0])
    x = Vec3(1, 0)
    y = Vec3(0, 1)

    phi = np.radians(30)
    R = Mat3x3.rotation(phi)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    i1 = R * x
    j1 = R * y


    def frame1(scene: Scene):
        # draw_arc(O, y, i1,
        #          radius=0.2,
        #          color="red",
        #          linestyle="--",
        #          linewidth=2.0,
        #          )

        print_label(start=np.array([1, 0]),
                    label=r"$i$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="grey",
                    label_offset=(-0.05, 0.05)
                    )

        print_label(start=np.array([0, 1]),
                    label=r"$j$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="grey",
                    label_offset=(0, 0.05)
                    )

        # Rotation
        print_label(start=np.array(j1.data[:2]),
                    label=r"$j'$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="green",
                    label_offset=(0, 0.05)
                    )

        print_label(start=np.array(i1.data[:2]),
                    label=r"$i'$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="red",
                    label_offset=(0, 0.05)
                    )

        draw_arc(O, y, j1,
                 radius=0.3,
                 color="green",
                 linestyle="--",
                 linewidth=2.0,
                 )

        draw_arc(O, x, i1,
                 radius=0.3,
                 color="green",
                 linestyle="--",
                 linewidth=2.0,
                 )

        lable_pos = (0.335, 0.06)
        print_label(start=lable_pos,
                    label=r"$\varphi$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="green"
                    )

        lable_pos = (-0.15, 0.35)
        print_label(start=lable_pos,
                    label=r"$\varphi$",
                    label_fontsize=LABEL_FONT_SIZE,
                    label_color="green"
                    )


    scene = Scene(
        coordinate_rect=(-0.9, -0.5, 1.2, 1.2),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        title="",
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        axis_color="grey",  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    scene["x"] = VectorModel(*x.xy, color="grey")
    scene["y"] = VectorModel(*y.xy, color="grey")
    scene["-i"] = LineModel(0, 0, -0.5, 0, line_style="--", color="grey")
    scene["-j"] = LineModel(0, 0, 0, -0.3, line_style="--", color="grey")

    scene["x1"] = VectorModel(*i1.xy, color="red")
    scene["y1"] = VectorModel(*j1.xy, color="green")

    i1_proj_i = x * cos_phi
    i1_proj_j = y * sin_phi
    scene["i1_proj_i"] = LineModel(i1, i1_proj_i, line_style="--", color="red")
    scene["i1_proj_j"] = LineModel(i1, i1_proj_j, line_style="--", color="red")

    j1_proj_i = -x * sin_phi
    j1_proj_j = y * cos_phi
    scene["j1_proj_i"] = LineModel(j1, j1_proj_i, line_style="--", color="green")
    scene["j1_proj_j"] = LineModel(j1, j1_proj_j, line_style="--", color="green")



    scene.add_frames(
        frame1
    )

    scene.show()
