import numpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from src.engine.scene.Scene import Scene


def draw_poly(plt_axis, vertices,
              alpha=1.0,
              edgecolor='black',
              facecolor="cyan"
              ):
    # Draw polygon
    polygon = Poly3DCollection([vertices], alpha=alpha, edgecolor=edgecolor, facecolor=facecolor)
    plt_axis.add_collection3d(polygon)


if __name__ == '__main__':
    def frame1(scene: Scene):
        vertices = [
            numpy.array((0, 0, 0)),
            numpy.array((1, 0, 0)),
            numpy.array((1, 1, 0)),
            numpy.array((0, 1, 0)),
        ]

        draw_poly(scene.plt_axis,
                  vertices,
                  edgecolor="green",
                  alpha=0.1,
                  facecolor="red"
                  )


    custom_scene = Scene(
        coordinate_rect=(0, 0, 0, 5, 5, 5),
    )
    custom_scene.add_frames(frame1)
    custom_scene.show()
