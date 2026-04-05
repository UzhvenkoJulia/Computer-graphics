import numpy as np

from src.engine.model.CoordinateFrame import CoordinateFrame
from src.engine.scene.Scene import Scene
from src.math.Mat3x3 import Mat3x3

RECT_KEY = "rect"

R = Mat3x3.rotation(np.radians(45))
S = Mat3x3.scale(0.5, 0.5)
T = Mat3x3.translation(1, 1)


############## Frame 1 ##################
def frame1(scene: Scene):
    rect: CoordinateFrame = scene[RECT_KEY]
    rect.line_style = "--"  # стиль ліній


############## Frame 2 ##################
def frame2(scene: Scene):
    rect: CoordinateFrame = scene[RECT_KEY]
    rect.transformation = R * S


############## Frame 3 ##################
def frame3(scene: Scene):
    rect: CoordinateFrame = scene[RECT_KEY]

    rect.alpha = 1.0
    rect.line_style = "solid"  # стиль ліній
    rect.transformation = T * R * S


simple_scene = Scene(
    coordinate_rect=(-1, -1, 3, 3),  # розмірність системи координатps
    grid_show=False,  # чи показувати координатну сітку
    base_axis_show=False,  # чи показувати базові осі зображення
    axis_show=True,  # чи показувати осі координат
    axis_color="grey",  # колір осей координат
    axis_line_style="-."  # стиль ліній осей координат
)

simple_scene[RECT_KEY] = CoordinateFrame()

simple_scene.add_frames(
    frame1,
    frame2,
    frame3,
)  # додаємо кадри на сцену

simple_scene.show()
