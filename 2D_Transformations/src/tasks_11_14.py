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

# ЗАВДАННЯ 11: Зворотна трансформація

class Task11Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # фінальні точки з умови задачі (зелений багатокутник)
        final_points = [(2, 3.4), (4.9, 4), (4.5, 6), (1.6, 5.4)]
        poly_final = Polygon(color="green", line_style="-", vertices_show=True)
        coords = []
        for p in final_points: coords.extend(p)
        poly_final.set_geometry(*coords)
        self["final"] = poly_final

        T = np.array([
            [2.934, -0.416, 2.000],
            [0.624,  1.956, 3.400],
            [0,      0,     1]
        ])
        
        T_inv = np.linalg.inv(T)
        
        poly_init = Polygon(color="red", line_style="--", vertices_show=True)
        poly_init.set_geometry(*apply_transformation(T_inv, final_points))
        self["init"] = poly_init

# ЗАВДАННЯ 12: Пастка (матриця з перекосом)

class Task12Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(*[c for p in INITIAL_POINTS for c in p])
        self["init"] = poly_init

        T = np.array([
            [0.866, 0.5, 4],
            [0.5, 0.866, 3],
            [0, 0, 1]
        ])
        
        poly_final = Polygon(color="red", vertices_show=True)
        poly_final.set_geometry(*apply_transformation(T, INITIAL_POINTS))
        self["final"] = poly_final

# ЗАВДАННЯ 13: Успішне розкладання

class Task13Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(*[c for p in INITIAL_POINTS for c in p])
        self["init"] = poly_init

        T = np.array([
            [1.414, -2.121, 1],
            [1.414,  2.121, 1],
            [0,      0,     1]
        ])
        
        poly_final = Polygon(color="purple", vertices_show=True)
        poly_final.set_geometry(*apply_transformation(T, INITIAL_POINTS))
        self["final"] = poly_final

# ЗАВДАННЯ 14: Розкладання з опорною точкою (1, 1)

class Task14Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = Polygon(color="blue", line_style="--", vertices_show=True)
        poly_init.set_geometry(*[c for p in INITIAL_POINTS for c in p])
        self["init"] = poly_init

        T = np.array([
            [1.732, -1,    5],
            [1,      1.732, -3],
            [0,      0,     1]
        ])
        
        poly_final = Polygon(color="orange", vertices_show=True)
        poly_final.set_geometry(*apply_transformation(T, INITIAL_POINTS))
        self["final"] = poly_final

        # опорна точка (1,1)
        pivot = Polygon(color="black", vertices_show=True)
        pivot.set_geometry(0.95, 0.95, 1.05, 0.95, 1.05, 1.05, 0.95, 1.05)
        self["pivot"] = pivot

if __name__ == '__main__':
    print("Запускаю Завдання 11...")
    Task11Scene(coordinate_rect=(-1, -1, 6, 7), title="Завдання 11: Зворотна трансформація", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 12...")
    Task12Scene(coordinate_rect=(-1, -1, 6, 6), title="Завдання 12: Матриця з перекосом", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 13...")
    Task13Scene(coordinate_rect=(-2, -1, 5, 5), title="Завдання 13: Розкладання", grid_show=True, axis_show=True).show()

    print("Запускаю Завдання 14...")
    Task14Scene(coordinate_rect=(-2, -4, 8, 3), title="Завдання 14: Розкладання з Pivot", grid_show=True, axis_show=True).show()