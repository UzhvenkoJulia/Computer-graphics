import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

# ЗАВДАННЯ 1: Композиція трансформацій

"""
МАТЕМАТИЧНІ РОЗРАХУНКИ ДЛЯ ЗАВДАННЯ 1:
Початковий квадрат: A(0,0), B(1,0), C(1,1), D(0,1)

Етап 1: Поворот на 30 градусів навколо початку координат.
Матриця повороту R30 (cos 30 = 0.866, sin 30 = 0.5):
|  0.866 -0.5    0 |
|  0.5    0.866  0 |
|  0      0      1 |
Проміжні координати (після повороту):
A1 = (0, 0)
B1 = (1*0.866 - 0*0.5, 1*0.5 + 0*0.866) = (0.866, 0.5)
C1 = (1*0.866 - 1*0.5, 1*0.5 + 1*0.866) = (0.366, 1.366)
D1 = (0*0.866 - 1*0.5, 0*0.5 + 1*0.866) = (-0.5, 0.866)

Етап 2: Переміщення на вектор (2, 3).
Матриця переміщення T:
    | 1  0  2 |
Т = | 0  1  3 |
    | 0  0  1 |
Фінальні координати (додаємо 2 до x, та 3 до y):
A2 = (0+2, 0+3) = (2, 3)
B2 = (0.866+2, 0.5+3) = (2.866, 3.5)
C2 = (0.366+2, 1.366+3) = (2.366, 4.366)
D2 = (-0.5+2, 0.866+3) = (1.5, 3.866)
"""

class Task1Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_initial = Polygon(color="blue", line_style="--", vertices_show=True)
        square_initial.set_geometry(
            0, 0,
            1, 0,
            1, 1,
            0, 1
        )
        self["initial_square"] = square_initial

        square_final = Polygon(color="red", line_style="-", vertices_show=True)
        square_final.set_geometry(
            2, 3,
            2.866, 3.5,
            2.366, 4.366,
            1.5, 3.866
        )
        self["final_square"] = square_final

if __name__ == '__main__':
    scene = Task1Scene(
        image_size=(6, 6),                 
        coordinate_rect=(-1, -1, 5, 5),    
        title="Завдання 1: Композиція трансформацій",
        grid_show=True,                    
        axis_show=True                     
    )
    scene.show()