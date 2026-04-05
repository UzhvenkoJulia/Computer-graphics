import matplotlib.pyplot as plt
import numpy

from src.base.points import draw_points
from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.engine.scene.Scene import Scene


def draw_poly(x, y=None,
              fill_color='none', alpha=1.0,
              vertices_show=False, vertex_color="black", vertex_size=50,
              edgecolor='black', linewidth=2, solid_line=False,
              labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,
              ):
    if y is None:
        x1 = []
        y1 = []
        for a, b in x:
            x1.append(a)
            y1.append(b)

        draw_poly(x1, y1, fill_color, alpha, vertices_show, vertex_color, vertex_size, edgecolor, linewidth, solid_line,
                  labels,
                  labels_color, labels_font_size)

        return

    plt.fill(x, y,
             facecolor=fill_color,
             alpha=alpha,
             edgecolor=edgecolor,
             linewidth=linewidth,
             )

    if solid_line:
        plt.fill(x, y,
                 facecolor="none",
                 edgecolor=edgecolor,
                 linewidth=linewidth,
                 )

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
            # Координати вершин багатокутника
            # x = [1, 3, 4, 2]
            # y = [1, 1, 3, 4]

            vertices = [
                numpy.array((1, 1)),
                numpy.array((3, 1)),
                numpy.array((4, 3)),
                numpy.array((2, 4)),
            ]

            labels = [
                ('A', (-0.3, -0.3)),  # name + offset
                ('B', (0.15, -0.3)),
                ('C', (0.1, 0.0)),
                ('D', (-0.1, 0.15))
            ]  # Підписи вершин
            draw_poly(
                # x, y,
                vertices,
                labels=labels,
                alpha=0.1,
                solid_line=True,
                vertices_show=True,
                vertex_size=100,
                vertex_color="red",
                linewidth=2,
                fill_color="red"
            )


    scene = Scene(
        coordinate_rect=(0, 0, 5, 5),
    )
    scene.add_frames(frame1)
    scene.show()
