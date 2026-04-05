import numpy as np

from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3
from src.base.axes import draw_axis
from src.engine.model.BaseModel import BaseModel


class CoordinateFrame(BaseModel):

    def __init__(self):
        super().__init__(
            0, 0,
            1, 0,
            0, 1,
        )

        self.color = ("red", "green")
        self.line_style = "-"
        self.line_width = 1.0
        self.head_width_coef = 0.05
        self.head_length_coef = 0.1

    def set_parameters(self,
                       color=None,
                       line_width=None,
                       line_style=None,
                       head_width_coef = None,
                       head_length_coef = None,
                       ):

        if color is not None:
            if isinstance(color, str):
                self.color = (color, color)
            elif isinstance(color, (tuple, list)) and len(color) == 2:
                self.color = tuple(color)  # колір осей координат

        if line_width is not None:
            self.line_width = line_width  # товщина осей координат
        if line_style is not None:
            self.line_style = line_style  # стиль ліній осей координат
        if head_width_coef is not None:
            self.head_width_coef = head_width_coef
        if head_length_coef is not None:
            self.head_length_coef = head_length_coef

    def draw_model(self):
        transformed_geometry = self.transformed_geometry
        ps = [el.xyz for el in transformed_geometry]

        origin = ps[0]
        ox = ps[1]
        oy = ps[2]

        draw_axis(
            origin, ox,
            color=self.color[0],
            linewidth=self.line_width,
            linestyle=self.line_style,
            head_length_coef=self.head_length_coef,
            head_width_coef=self.head_width_coef,
        )

        draw_axis(
            origin, oy,
            color=self.color[1],
            linewidth=self.line_width,
            linestyle=self.line_style,
            head_length_coef=self.head_length_coef,
            head_width_coef=self.head_width_coef,
        )


if __name__ == '__main__':
    RECT_KEY = "rect"

    R = Mat3x3.rotation(np.radians(30))
    S = Mat3x3.scale(0.5, 0.5)
    T = Mat3x3.translation(1, 0.5)


    ############## Frame 1 ##################
    def frame1(scene: Scene):
        rect: CoordinateFrame = scene[RECT_KEY]
        rect.line_style = "--"  # стиль ліній
        # rect.transformation = T * R #* S


    simple_scene = Scene(
        coordinate_rect=(-1, -1, 3, 3),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color="grey",  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    simple_scene[RECT_KEY] = CoordinateFrame()
    simple_scene.add_frames(frame1)

    simple_scene.show()