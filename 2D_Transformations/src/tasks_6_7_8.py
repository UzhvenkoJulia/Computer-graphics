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

INITIAL_POINTS = [(0, 0), (1, 0), (1, 1), (0, 1)]

# ЗАВДАННЯ 6: Композиція трьох трансформацій (ПОРЯДОК МАЄ ЗНАЧЕННЯ)

class Task6Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Початковий квадрат
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(0,0, 1,0, 1,1, 0,1)
        self["init"] = poly_init

        S = np.array([[1, 0, 0], [0, 3, 0], [0, 0, 1]]) 
        angle = np.radians(60)
        R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        T = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]]) # переміщення (2, 3)

        # Розтяг -> Поворот -> Переміщення (червоний)
        M1 = T @ R @ S
        poly1 = Polygon(color="red", vertices_show=True)
        poly1.set_geometry(*apply_transformation(M1, INITIAL_POINTS))
        self["order1"] = poly1

        # Переміщення -> Розтяг -> Поворот (зелений)
        M2 = R @ S @ T
        poly2 = Polygon(color="green", vertices_show=True)
        poly2.set_geometry(*apply_transformation(M2, INITIAL_POINTS))
        self["order2"] = poly2

# ЗАВДАННЯ 7: Поворот навколо опорної точки (Pivot)

class Task7Scene(Scene):
    def __init__(self, pivot=(0.5, 0.5), **kwargs):
        super().__init__(**kwargs)
        px, py = pivot
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(0,0, 1,0, 1,1, 0,1)
        self["init"] = poly_init
        
        # Pivot: Translate Back * Rotate * Translate to Origin
        T_to_origin = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
        angle = np.radians(60)
        R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        T_back = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]])
        
        M_total = T_back @ R @ T_to_origin
        
        poly_final = Polygon(color="red", vertices_show=True)
        poly_final.set_geometry(*apply_transformation(M_total, INITIAL_POINTS))
        self["final"] = poly_final
        
        # опорна точка (маленький чорний квадратик)
        pivot_point = Polygon(color="black", vertices_show=True)
        pivot_point.set_geometry(px-0.05, py-0.05, px+0.05, py-0.05, px+0.05, py+0.05, px-0.05, py+0.05)
        self["pivot"] = pivot_point

# ЗАВДАННЯ 8: Розтяг навколо опорної точки (Pivot)

class Task8Scene(Scene):
    def __init__(self, pivot=(0.5, 0.5), **kwargs):
        super().__init__(**kwargs)
        px, py = pivot
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(0,0, 1,0, 1,1, 0,1)
        self["init"] = poly_init

        T_to_origin = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
        S = np.array([[2, 0, 0], [0, 3, 0], [0, 0, 1]]) # x*2, y*3
        T_back = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]])

        M_total = T_back @ S @ T_to_origin
        
        poly_final = Polygon(color="green", vertices_show=True)
        poly_final.set_geometry(*apply_transformation(M_total, INITIAL_POINTS))
        self["final"] = poly_final
        
        pivot_p = Polygon(color="black", vertices_show=True)
        pivot_p.set_geometry(px-0.05, py-0.05, px+0.05, py-0.05, px+0.05, py+0.05, px-0.05, py+0.05)
        self["pivot"] = pivot_p

if __name__ == '__main__':
    print("Запускаю Завдання 6...")
    Task6Scene(coordinate_rect=(-5, -5, 8, 8), title="Завдання 6: Порядок трансформацій", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 7 (3 вікна по черзі)...")
    for p in [(0.5, 0.5), (0, 1), (1, 1)]:
        Task7Scene(pivot=p, coordinate_rect=(-2, -2, 4, 4), title=f"Завдання 7: Поворот навколо {p}", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 8 (3 вікна по черзі)...")
    for p in [(0.5, 0.5), (0, 1), (1, 1)]:
        Task8Scene(pivot=p, coordinate_rect=(-3, -3, 6, 6), title=f"Завдання 8: Розтяг відносно {p}", grid_show=True, axis_show=True).show()