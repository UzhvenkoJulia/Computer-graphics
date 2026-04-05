import numpy as np

from src.base.arc import draw_fake_rectangular_arc
from src.base.text import print_label
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene

O = np.array([0, 0])
x = np.array([1, 0])  # Перший вектор
y = np.array([0, 1])  # Другий вектор
c = 2 * x + 0.5 * y

RECT_KEY = "coord_frame"
if __name__ == '__main__':
    ############## Frame 1 ##################
    def frame1(scene: Scene):
        v_x: VectorModel = scene["x"]
        v_x["color"] = "red"


        v_y: VectorModel = scene["y"]
        v_y["color"] = "green"


        draw_fake_rectangular_arc(O, x, y,
                                  scale=0.2,
                                  color="blue",
                                  linestyle="--", linewidth=1.0,
                                  )

        print_label(start=x,
                    label=r"$x$",
                    label_offset=(-0.1, 0.1)
                    )

        print_label(start=y,
                    label=r"$y$",
                    label_offset=(-0.15, -0.05)
                    )

    simple_scene = Scene(
        coordinate_rect=(-1, -1, 2, 2),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=True,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        axis_color="grey",  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    simple_scene["x"] = VectorModel(x)
    simple_scene["y"] = VectorModel(y)

    simple_scene.add_frames(
        frame1,
    )



    simple_scene.show()

