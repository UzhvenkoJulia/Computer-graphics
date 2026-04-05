import numpy as np

from src.base.arc import draw_fake_rectangular_arc
from src.base.text import print_label
from src.engine.model.CoordinateFrame import CoordinateFrame
from src.engine.scene.Scene import Scene

O = np.array([0, 0])
v1 = np.array([1, 0])  # Перший вектор
v2 = np.array([0, 1])  # Другий вектор

RECT_KEY = "coord_frame"
if __name__ == '__main__':
    ############## Frame 1 ##################
    def frame1(scene: Scene):
        frame: CoordinateFrame = scene[RECT_KEY]


        draw_fake_rectangular_arc(O, v1, v2,
                                  scale=0.2,
                                  color="blue",
                                  linestyle="--", linewidth=2.0,
                                  )

        print_label(start=v1,
                    label=r"$x$",
                    label_offset=(0.1, 0.1)
                    )

        print_label(start=v2,
                    label=r"$y$",
                    label_offset=(-0.2, 0.1)
                    )




    simple_scene = Scene(
        coordinate_rect=(-1, -1, 2, 2),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=True,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        axis_color="grey",  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    coord_frame = CoordinateFrame()
    coord_frame.set_parameters(
        line_width=3.0,
        head_width_coef=0.03,
        head_length_coef=0.05,
    )
    simple_scene[RECT_KEY] = coord_frame


    simple_scene.add_frames(
        frame1,
    )



    simple_scene.show()

