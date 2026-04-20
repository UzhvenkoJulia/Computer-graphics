from src.base.text import print_label
from src.engine.model.Vector import Vector
from src.engine.scene.Scene import Scene

O = (0, 0, 0)
x = (1, 0, 0)
y = (0, 1, 0)
z = (0, 0, 1)
OX = "OX"
OY = "OY"
OZ = "OZ"


class VectorScene(Scene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ox = Vector(
            O, x,
            color="red"
        )
        self[OX] = ox
        ox.linewidth = 3

        oy = Vector(
            O, y,
            color="green"
        )
        self[OY] = oy
        oy.linewidth = 3

        oz = Vector(
            O, z,
            color="blue"
        )
        self[OZ] = oz
        oz.linewidth = 3


if __name__ == '__main__':
    def frame1(scene):
        print_label(
            scene.plt_axis,
            start=O,
            label=r"$0$", label_color="black", label_fontsize=22,
            label_offset=(0.0, -0.4, 0.0))

        print_label(
            scene.plt_axis,
            start=x,
            label=r"$x$", label_color="red", label_fontsize=22,
            label_offset=(0., -0.3, 0.0))

        print_label(
            scene.plt_axis,
            start=y,
            label=r"$y$", label_color="green", label_fontsize=22,
            label_offset=(0.1, 0., 0.0))

        print_label(
            scene.plt_axis,
            start=z,
            label=r"$z$", label_color="blue", label_fontsize=22,
            label_offset=(0.0, -0.3, 0.3))


    scene = VectorScene(
        image_size=(10, 10),  # image size: 1 - 100 pixels
        coordinate_rect=(-1, -1, -1, 3, 3, 3),  # coordinate system dimensions
        title="3D coordinate system",  # figure title
        # base_axis_show=True,  # whether to show base image axes
        # grid_show=True,  # whether to show the coordinate grid
        # axis_show=False,  # whether to show coordinate axes
        axis_color=("grey", "grey", "grey"),  # coordinate axis color
        axis_line_width=2.0,
        axis_line_style="--",  # coordinate axis line style
        axis_show_from_origin=True,
    )

    scene.add_frames(frame1)

    scene.show()
