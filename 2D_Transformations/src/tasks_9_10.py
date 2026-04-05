import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

def apply_transformation(matrix, points):
    result_coords = []
    for x, y in points:
        vec = np.array([x, y, 1])
        new_vec = matrix.dot(vec)
        result_coords.extend([float(new_vec[0]), float(new_vec[1])])
    return result_coords

def T_mat(dx, dy):
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

def S_mat(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def R_mat(angle_deg):
    rad = np.radians(angle_deg)
    return np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])

INITIAL_POINTS = [(0, 0), (1, 0), (1, 1), (0, 1)]

# ЗАВДАННЯ 9: Розтяг і переміщення з опорною точкою

class Task9Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(*[coord for pt in INITIAL_POINTS for coord in pt])
        self["init"] = poly_init

        pivot_x, pivot_y = 1, 1
        T_to_pivot = T_mat(pivot_x, pivot_y)     # переміщення ДО опорної точки
        T_from_pivot = T_mat(-pivot_x, -pivot_y) # переміщення ВІД опорної точки
        
        S = S_mat(2, 1)                         
        T_move = T_mat(3, -2)                   

        S_pivot = T_to_pivot @ S @ T_from_pivot

        # 1: Розтяг (відносно pivot) -> Переміщення (червоний)
        M1 = T_move @ S_pivot
        poly1 = Polygon(color="red", vertices_show=True)
        poly1.set_geometry(*apply_transformation(M1, INITIAL_POINTS))
        self["order1"] = poly1

        # 2: Переміщення -> Розтяг (відносно pivot) (зелений)
        M2 = S_pivot @ T_move
        poly2 = Polygon(color="green", vertices_show=True)
        poly2.set_geometry(*apply_transformation(M2, INITIAL_POINTS))
        self["order2"] = poly2

        pivot_point = Polygon(color="black", vertices_show=True)
        pivot_point.set_geometry(0.95, 0.95, 1.05, 0.95, 1.05, 1.05, 0.95, 1.05)
        self["pivot"] = pivot_point

# ЗАВДАННЯ 10: Зсув і масштабування (3 порядки!)

class Task10Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(*[coord for pt in INITIAL_POINTS for coord in pt])
        self["init"] = poly_init

        pivot_x, pivot_y = 0.5, 0.5
        T_to_p = T_mat(pivot_x, pivot_y)
        T_from_p = T_mat(-pivot_x, -pivot_y)

        # Scale та Rotate
        S_pivot = T_to_p @ S_mat(2, 2) @ T_from_p
        R_pivot = T_to_p @ R_mat(30) @ T_from_p
        
        T_move = T_mat(1, -1)

        # Масштабування -> Обертання -> Зсув (червоний)
        M1 = T_move @ R_pivot @ S_pivot
        poly1 = Polygon(color="red", vertices_show=True)
        poly1.set_geometry(*apply_transformation(M1, INITIAL_POINTS))
        self["order1"] = poly1

        # Зсув -> Масштабування -> Обертання (зелений)
        M2 = R_pivot @ S_pivot @ T_move
        poly2 = Polygon(color="green", vertices_show=True)
        poly2.set_geometry(*apply_transformation(M2, INITIAL_POINTS))
        self["order2"] = poly2

        # Масштабування -> Зсув -> Обертання (фіолетовий)
        M3 = R_pivot @ T_move @ S_pivot
        poly3 = Polygon(color="purple", vertices_show=True)
        poly3.set_geometry(*apply_transformation(M3, INITIAL_POINTS))
        self["order3"] = poly3

        pivot_point = Polygon(color="black", vertices_show=True)
        pivot_point.set_geometry(0.45, 0.45, 0.55, 0.45, 0.55, 0.55, 0.45, 0.55)
        self["pivot"] = pivot_point

if __name__ == '__main__':
    print("Запускаю Завдання 9...")
    Task9Scene(coordinate_rect=(-3, -3, 8, 8), title="Завдання 9: Розтяг і переміщення (Pivot)", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 10...")
    Task10Scene(coordinate_rect=(-4, -4, 6, 6), title="Завдання 10: 3 порядки трансформацій", grid_show=True, axis_show=True).show()