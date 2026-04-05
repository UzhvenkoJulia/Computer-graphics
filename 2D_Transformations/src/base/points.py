import numpy as np
from matplotlib import pyplot as plt

from src.base.text import DEFAULT_LABEL_FONT_SIZE, print_label
from src.engine.scene.Scene import Scene


def draw_point(start, size=50, color="black",
               label="", label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0)):
    plt.scatter(*start, color=color, label=label, s=size)  # s - розмір точки

    print_label(start=start, label=label, label_color=label_color, label_fontsize=label_fontsize,
                label_offset=label_offset)


def draw_points(
        x, y=None,
        vertices_show=True, vertex_color="black", vertex_size=50,
        labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,
):
    if y is None:
        x1 = []
        y1 = []
        for a, b in x:
            x1.append(a)
            y1.append(b)

        draw_points(x1, y1,
                    vertices_show=vertices_show,
                    vertex_color=vertex_color,
                    vertex_size=vertex_size,
                    labels=labels,
                    labels_color=labels_color,
                    labels_font_size=labels_font_size,
                    )

        return

    if vertices_show:
        # Малювання точок вершин
        plt.scatter(x, y, color=vertex_color, s=vertex_size, zorder=5)

    if labels is None or len(labels) == 0:
        return

    # Додавання підписів
    for i, lab in enumerate(labels):
        label = ""
        label_offset = (0, 0)

        if isinstance(lab, str):
            label = lab
        elif isinstance(lab, (list, tuple)):
            if len(lab) >= 1:
                label = lab[0]
            if len(lab) >= 2:
                offset = lab[1]
                if isinstance(offset, (list, tuple)):
                    offset = np.array(offset, dtype=float)
                    if offset.shape == (2,):
                        label_offset = offset

        print_label((x[i], y[i]),
                    label=label,
                    label_offset=label_offset,
                    label_fontsize=labels_font_size,
                    label_color=labels_color,
                    )


if __name__ == '__main__':


    def frame1(scene):
            p1 = np.array([0.2, .2])

            draw_point(p1, size=100, color="blue", label=r"$R$", label_color="blue", label_offset=(-0.02, 0.05))

            points = (
                (-1, 2), (-1, 3), (3, 1), (2, -3), (-3, -2)
            )

            draw_points(points,
                        vertices_show=True,
                        labels=[('A', (-0.1, -0.6)),
                                ('B', (-0.1, 0.1)),
                                'C',
                                "D",
                                # "Hello"
                                ("H",)
                                ],  # Підписи вершин
                        vertex_color="red",
                )

    scene = Scene(
        coordinate_rect=(-4, -4, 4, 4),
        # grid_show=False,
        grid_line_linestyle="-.",
        axis_show=True,
        base_axis_show=False,
    )
    scene.add_frames(frame1)
    scene.show()
