import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

# ЗАВДАННЯ 2: Розтяг і поворот

"""
МАТЕМАТИЧНІ РОЗРАХУНКИ ДЛЯ ЗАВДАННЯ 2:
Початковий квадрат: A(0,0), B(1,0), C(1,1), D(0,1)

Етап 1: Розтяг по осі x у 2 рази.
Матриця масштабування S:
| 2  0  0 |
| 0  1  0 |
| 0  0  1 |
Проміжні координати (прямокутник): A1(0,0), B1(2,0), C1(2,1), D1(0,1)

Етап 2: Поворот на 45 градусів.
Матриця повороту R45 (cos 45 = 0.707, sin 45 = 0.707):
|  0.707 -0.707  0 |
|  0.707  0.707  0 |
|  0      0      1 |
Фінальні координати (множимо проміжні на матрицю повороту):
A2 = (0, 0)
B2 = (2*0.707, 2*0.707) = (1.414, 1.414)
C2 = (2*0.707 - 1*0.707, 2*0.707 + 1*0.707) = (0.707, 2.121)
D2 = (-0.707, 0.707)
"""

class Task2Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_init = Polygon(color="blue", line_style="--", vertices_show=True)
        square_init.set_geometry(0, 0, 1, 0, 1, 1, 0, 1)
        self["initial"] = square_init

        square_final = Polygon(color="red", line_style="-", vertices_show=True)
        square_final.set_geometry(
            0, 0,
            1.414, 1.414,
            0.707, 2.121,
            -0.707, 0.707
        )
        self["final"] = square_final


# ЗАВДАННЯ 3: Поворот і переміщення

"""
МАТЕМАТИЧНІ РОЗРАХУНКИ ДЛЯ ЗАВДАННЯ 3:
Початковий квадрат: A(0,0), B(1,0), C(1,1), D(0,1)

Етап 1: Поворот на 90 градусів.
Матриця повороту R90 (cos 90 = 0, sin 90 = 1):
|  0 -1  0 |
|  1  0  0 |
|  0  0  1 |
Проміжні координати: A1(0,0), B1(0,1), C1(-1,1), D1(-1,0)

Етап 2: Переміщення на вектор (2, 3).
Матриця переміщення T:
| 1  0  2 |
| 0  1  3 |
| 0  0  1 |
Фінальні координати (додаємо 2 до x, та 3 до y):
A2 = (0+2, 0+3) = (2, 3)
B2 = (0+2, 1+3) = (2, 4)
C2 = (-1+2, 1+3) = (1, 4)
D2 = (-1+2, 0+3) = (1, 3)
"""

class Task3Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_init = Polygon(color="blue", line_style="--", vertices_show=True)
        square_init.set_geometry(0, 0, 1, 0, 1, 1, 0, 1)
        self["initial"] = square_init

        square_final = Polygon(color="green", line_style="-", vertices_show=True)
        square_final.set_geometry(
            2, 3,
            2, 4,
            1, 4,
            1, 3
        )
        self["final"] = square_final


if __name__ == '__main__':
    scene2 = Task2Scene(
        image_size=(5, 5), coordinate_rect=(-2, -1, 3, 4), 
        title="Завдання 2: Розтяг і поворот", grid_show=True, axis_show=True
    )
    print("Відкриваю Завдання 2... Закрийте віконце, щоб перейти до Завдання 3")
    scene2.show()  

    scene3 = Task3Scene(
        image_size=(5, 5), coordinate_rect=(-2, -1, 4, 5), 
        title="Завдання 3: Поворот і переміщення", grid_show=True, axis_show=True
    )
    print("Відкриваю Завдання 3...")
    scene3.show()