import numpy as np

from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

FIGURE_KEY = "figure"
R = Mat3x3.rotation(np.radians(45))
S = Mat3x3.scale(2, 3)
T = Mat3x3.translation(0.5, 0.9)


def frame1(scene):
    rect = scene[FIGURE_KEY]
    rect.color = "grey"  # колір ліній
    rect.line_style = "-."  # стиль ліній


def frame2(scene):
    rect = scene[FIGURE_KEY]
    rect.transformation = S
    rect.color = "red"
    rect.line_style = "--"  # стиль ліній


def frame3(scene):
    rect = scene[FIGURE_KEY]
    rect.line_style = "-"  # стиль ліній
    rect.transformation = R * S


def frame4(scene):
    rect = scene[FIGURE_KEY]
    rect.transformation = R
    rect.color = "green"
    rect.line_style = "--"  # стиль ліній


def frame5(scene):
    rect = scene[FIGURE_KEY]
    rect.transformation = (T * R * S)
    rect.color = "orange"
    rect.line_style = "-."  # стиль ліній


scene = Scene(
    coordinate_rect=(-3, -1, 3, 5),  # розмірність системи координат
    title="Picture",  # заголовок рисунка
    grid_show=False,  # чи показувати координатну сітку
    base_axis_show=False,  # чи показувати базові осі зображення
    axis_show=True,  # чи показувати осі координат
    axis_color=("red", "green"),  # колір осей координат
    axis_line_style="-."  # стиль ліній осей координат
)

scene[FIGURE_KEY] = Polygon(
    0, 0,
    1, 0,
    1, 1,
    0, 1,
)

scene.add_frames(frame1,
                 frame2,
                 frame3,
                 frame4,
                 frame5,
                 )
scene.show()
