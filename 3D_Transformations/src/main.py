from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    FIGURE_KEY = "polygon"

    scene = Scene(
        image_size=(5, 5),  # image size: 1 - 100 pixels
        coordinate_rect=(-1, -1, -1, 3, 3, 3),  # coordinate system dimensions
        title="3D coordinate system",  # figure title
        # base_axis_show=True,  # whether to show base image axes
        grid_show=True,  # whether to show the coordinate grid
        # axis_show=False,  # whether to show coordinate axes
        # axis_color=("red", "green", "blue"),  # coordinate axis color
        axis_line_width=1.0,
        axis_line_style="--",  # coordinate axis line style
        axis_show_from_origin=True,
    )

    scene.show()
