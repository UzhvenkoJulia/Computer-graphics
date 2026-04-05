import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

def apply_transformation(matrix, points):
    """
    Бере набір точок виду [(x1,y1), (x2,y2)...] і матрицю трансформації.
    Повертає список координат для рушія: [x1_new, y1_new, x2_new, y2_new...]
    """
    result_coords = []
    for x, y in points:
        vec = np.array([x, y, 1])
        new_vec = matrix.dot(vec)
        result_coords.extend([float(new_vec[0]), float(new_vec[1])])
    return result_coords

INITIAL_POINTS = [(0, 0), (1, 0), (1, 1), (0, 1)]

# ЗАВДАННЯ 4: Розтяг і поворот

"""
МАТЕМАТИКА (Завдання 4):
1. Розтяг по осі y у 3 рази:
| 1  0  0 |
| 0  3  0 |
| 0  0  1 |

2. Поворот на 60° (cos 60 = 0.5, sin 60 = 0.866):
|  0.5 -0.866  0 |
|  0.866 0.5   0 |
|  0     0     1 |
"""
class Task4Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_init = Polygon(color="blue", line_style="--", vertices_show=True)
        square_init.set_geometry(0, 0, 1, 0, 1, 1, 0, 1)
        self["initial"] = square_init

        S_y = np.array([
            [1, 0, 0],
            [0, 3, 0],
            [0, 0, 1]
        ])
        
        angle = np.radians(60) 
        R_60 = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle),  np.cos(angle), 0],
            [0,              0,             1]
        ])

        # Композиція матриць: множення повороту на розтяг (M = R * S)
        # У numpy @ - множення матриць
        M_total = R_60 @ S_y

        final_coords = apply_transformation(M_total, INITIAL_POINTS)

        square_final = Polygon(color="red", line_style="-", vertices_show=True)
        square_final.set_geometry(*final_coords)
        self["final"] = square_final

# ЗАВДАННЯ 5: Переміщення і масштабування

"""
МАТЕМАТИКА (Завдання 5):
1. Переміщення на (1, -1):
| 1  0  1 |
| 0  1 -1 |
| 0  0  1 |

2. Масштабування по обох осях у 2 рази:
| 2  0  0 |
| 0  2  0 |
| 0  0  1 |
"""
class Task5Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_init = Polygon(color="blue", line_style="--", vertices_show=True)
        square_init.set_geometry(0, 0, 1, 0, 1, 1, 0, 1)
        self["initial"] = square_init

        T = np.array([
            [1, 0,  1],
            [0, 1, -1],
            [0, 0,  1]
        ])

        S_xy = np.array([
            [2, 0, 0],
            [0, 2, 0],
            [0, 0, 1]
        ])

        # спочатку переміщення, потім масштабування (M = S * T)
        M_total = S_xy @ T

        final_coords = apply_transformation(M_total, INITIAL_POINTS)

        square_final = Polygon(color="green", line_style="-", vertices_show=True)
        square_final.set_geometry(*final_coords)
        self["final"] = square_final


if __name__ == '__main__':
    scene4 = Task4Scene(
        image_size=(5, 5), coordinate_rect=(-3, -1, 3, 5), 
        title="Завдання 4: Розтяг по Y і поворот", grid_show=True, axis_show=True
    )
    print("Відкриваю Завдання 4... Закрийте віконце, щоб перейти до Завдання 5")
    scene4.show()

    scene5 = Task5Scene(
        image_size=(5, 5), coordinate_rect=(-1, -3, 5, 3), 
        title="Завдання 5: Переміщення і масштабування", grid_show=True, axis_show=True
    )
    print("Відкриваю Завдання 5...")
    scene5.show()