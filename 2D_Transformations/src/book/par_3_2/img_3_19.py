import numpy as np

from src.base.arc import draw_arc
from src.base.text import print_label
from src.engine.model.Axis import Axis
from src.engine.model.LineModel import LineModel
from src.engine.scene.Scene import Scene

LABEL_FONT_SIZE = 20

if __name__ == '__main__':

    simple_scene = Scene(
        coordinate_rect=(-3.5, -3.5, 4, 3.5),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
    )

    orig = 0, 0
    x_dir = 3.1, 0
    z_dir = -1.4, -1.2
    y_dir = 0, 2.4
    v_dir = np.array([1.6, 0.9])
    v_arrow = v_dir + (0.14, 0.07)
    v_proj_vert =  1.7, -0.8
    v_proj_oxy_ccords =  1.7, -0.8
    v_proj_z_coord = -0.9, -0.8
    v_proj_x_coord = 2.8, 0.0
    v_proj_y_coord =  (0.0, 0.8 + 0.9 + 0.15)
    label_v_x_coord = 0.2, -1.1
    label_v_y_coord = -0.4, 0.9
    label_v_z_coord = 2.45, -0.6

    Ox = Axis(x_dir, color="red", linewidth=1.5, label="$x$", label_offset=(0.1, 0.1))
    Oy = Axis(y_dir, color="green", linewidth=1.5, label="$y$", label_offset=(0.1, 0.2))
    Oz = Axis(z_dir, color="blue", linewidth=1.5, label="$z$", label_offset=(-0.35, -0.3))
    v = Axis(v_dir, color="brown", linewidth=1.5, label="$v$", label_offset=(0.1, 0.2))
    v_proj_v = LineModel(v_arrow, v_proj_vert, color="black", linewidth=1., line_style="--", )
    v_proj_oxy = LineModel((0, 0), v_proj_oxy_ccords, color="black", linewidth=1., line_style="--", )
    v_proj_z = LineModel(v_proj_oxy_ccords, v_proj_z_coord, color="black", linewidth=1., line_style="--", )
    v_proj_x = LineModel(v_proj_oxy_ccords, v_proj_x_coord, color="black", linewidth=1., line_style="--", )
    v_proj_y = LineModel(v_arrow, v_proj_y_coord, color="black", linewidth=1., line_style="--", )

    def frame1(scene: Scene):
        draw_arc(orig, z_dir, v_proj_oxy_ccords,
                 radius=0.25,
                 color="blue",
                 linestyle="--",
                 linewidth=2.0,
                 )

        print_label(start= orig,
                    label=r"$\varphi$",
                    label_offset=(-0.1, -0.5),
                    label_fontsize=LABEL_FONT_SIZE,
                    )

        # draw_arc(orig, y_dir, v_dir,
        #          radius=0.35,
        #          color="green",
        #          linestyle="--",
        #          linewidth=2.0,
        #          )
        #
        # print_label(start= orig,
        #             label=r"$\theta$",
        #             label_offset=(0.1, 0.45),
        #             label_fontsize=LABEL_FONT_SIZE,
        #             )

        print_label(start= label_v_x_coord,
                    label=r"$v_x$",
                    label_color="red",
                    label_fontsize=LABEL_FONT_SIZE,
                    )

        print_label(start= label_v_y_coord,
                    label=r"$v_y$",
                    label_color="green",
                    label_fontsize=LABEL_FONT_SIZE,
                    )

        print_label(start= label_v_z_coord,
                    label=r"$v_z$",
                    label_color="blue",
                    label_fontsize=LABEL_FONT_SIZE,
                    )

    simple_scene["OX"] = Ox
    simple_scene["OY"] = Oy
    simple_scene["OZ"] = Oz
    simple_scene["v"] = v
    simple_scene["v_proj_v"] = v_proj_v
    simple_scene["v_proj_oxy"] = v_proj_oxy
    simple_scene["v_proj_z"] = v_proj_z
    simple_scene["v_proj_x"] = v_proj_x
    simple_scene["v_proj_y"] = v_proj_y

    simple_scene.add_frames(frame1)


    simple_scene.show()