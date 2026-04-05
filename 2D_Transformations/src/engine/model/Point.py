import numpy as np

from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.base.points import draw_points
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

DEFAULT_POINT_SIZE = 50
class SimplePoint(Model):

    def __init__(self, *vertices,
                 color="black",
                 vertex_size=DEFAULT_POINT_SIZE,
                 labels=("",),
                 label_color="black",
                 label_fontsize=DEFAULT_LABEL_FONT_SIZE,
                 ):
        super().__init__(*vertices)  # TODO:
        self.color = color
        self.vertex_size = vertex_size
        self.labels = labels
        self.label_color = label_color
        self.label_fontsize = label_fontsize

    def draw_model(self):
        transformed_geometry = self.transformed_geometry
        ps = [el.xy for el in transformed_geometry]

        draw_points(ps, vertex_color=self.color,
                    vertex_size=self.vertex_size,
                    labels=self.labels,
                    labels_color=self.label_color,
                    labels_font_size=self.label_fontsize,
                    )

    def __setitem__(self, key, value):
        if key == "labels":
            self.labels = value
            return
        if key == "label_color":
            self.label_color = value
            return
        if key == "label_fontsize":
            self.label_fontsize = value
            return

        super().__setitem__(key, value)

if __name__ == '__main__':
    scene_figure_key = "point"


    class SimplePointScene(Scene):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            point = SimplePoint(1, 1, 2, 2, 0, 1)
            point["labels"] = (
                ("$P_1$", (0, 0.2)),
                ("$P_2$", (0, 0.2)),
                ("$P_3$", (0, 0.2)),
            )
            point["label_offset"] = -0.3, 0.1
            point["label_color"] = "green"
            point["label_fontsize"] = 22
            self[scene_figure_key] = point


    def frame1(scene: Scene):
        point = scene[scene_figure_key]
        point.color = "blue"  # колір ліній


    def frame2(scene: Scene):
        point = scene[scene_figure_key]
        R = Mat3x3.rotation(np.radians(45))
        S = Mat3x3.scale(2, 3)
        T = Mat3x3.translation(1, 1)

        point.color = "red"  # колір ліній
        point.transformation = T * R * S


    scene = SimplePointScene(
        image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-2, -2, 6, 6),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    scene.add_frames(frame1,
                     frame2
                     )

    scene.show()
