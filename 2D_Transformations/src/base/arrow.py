import numpy as np
from matplotlib import pyplot as plt

from src.base.text import DEFAULT_LABEL_FONT_SIZE, print_label
from src.engine.scene.Scene import Scene


def draw_vector(p, u,
                color="black",
                label="", label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0)):
    # малювання вектора
    plt.quiver(p[0], p[1], u[0], u[1],
               angles='xy',
               scale_units='xy',
               scale=1,
               color=color, )

    print_label(start=np.array(p) + u * 0.5,
                label=label,
                label_color=label_color,
                label_fontsize=label_fontsize,
                label_offset=label_offset)


def draw_segment(start, end,
                 color="black",
                 label="", label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0)):
    # малювання вектора
    p = start
    u = end - start
    draw_vector(p, u, color, label, label_color, label_fontsize, label_offset)


def draw_arrow(p, u,
               color="black", linewidth=2.0,
               head_width=0.01, head_length=0.01, head_color="black",
               label="", label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0)):
    # малювання вектора
    plt.arrow(
        p[0], p[1], u[0], u[1],
        head_width=head_width, head_length=head_length,
        fc=head_color, ec=color, linewidth=linewidth
    )

    print_label(start=np.array(p) + u * 0.5,
                label=label,
                label_color=label_color,
                label_fontsize=label_fontsize,
                label_offset=label_offset)


if __name__ == '__main__':
    def frame1(scene):
        p1 = np.array([0.2, .2])
        u1 = np.array([0.6, 0.2])
        draw_vector(p1, u1, color="green", label=r"$T$",
                    label_color="red",
                    label_offset=(-0.05, 0.02),
                    )

        p2 = p1 - (0.0, 0.15)

        draw_arrow(p2, u1, color="green", label=r"$T$",
                   label_color="red",
                   label_offset=(-0.05, 0.02),
                   linewidth=2,
                   head_width=0.1,
                   head_length=0.1,
                   head_color="red"
                   )


    scene = Scene(
        coordinate_rect=(0, 0, 1, 1),
    )
    scene.add_frames(frame1)
    scene.show()
