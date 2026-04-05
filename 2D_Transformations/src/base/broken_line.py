from matplotlib import pyplot as plt

from src.base.points import draw_points
from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.engine.scene.Scene import Scene


def draw_broken_line(
        x, y=None,
        color="black",
        linewidth=1.0, line_style="solid",
        vertices_show=False, vertex_color="black", vertex_size=50,
        labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,
):
    if y is None:
        x1 = []
        y1 = []
        for a, b in x:
            x1.append(a)
            y1.append(b)

        draw_broken_line(x1, y1,
                         color=color,
                         vertices_show=vertices_show,
                         vertex_color=vertex_color,
                         vertex_size=vertex_size,
                         linewidth=linewidth,
                         line_style=line_style,
                         labels=labels,
                         labels_color=labels_color,
                         labels_font_size=labels_font_size,
                         )

        return

    plt.plot(x, y,
             color=color,
             linewidth=linewidth,
             linestyle=line_style)

    draw_points(x, y,
                vertices_show=vertices_show,
                vertex_color=vertex_color,
                vertex_size=vertex_size,
                labels=labels,
                labels_color=labels_color,
                labels_font_size=labels_font_size,
                )


if __name__ == '__main__':

    def frame1(self):
            points = (
                (-1, 2), (-1, 3), (3, 1), (2, -3), (-3, -2)
            )

            draw_broken_line(points,
                             color="blue",
                             line_style="--",
                             linewidth=1.0,
                             vertices_show=True,
                             labels=[('A', (-0.1, -0.6)),
                                     ('B', (-0.15, 0.2)),
                                     'C',
                                     "D",
                                     ("H", (-0.2, 0.15))
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


