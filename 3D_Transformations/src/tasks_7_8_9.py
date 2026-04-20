import numpy as np
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

def apply_transformation_3d(matrix, points):
    result_coords = []
    for p in points:
        vec = np.array([p[0], p[1], p[2], 1])
        new_vec = matrix.dot(vec)
        result_coords.extend([float(new_vec[0]), float(new_vec[1]), float(new_vec[2])])
    return result_coords

def T_mat3d(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def S_mat3d(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0,  1]
    ])

def R_x_mat3d(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

def R_y_mat3d(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

def R_z_mat3d(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

def R_arbitrary_mat3d(axis, angle_deg):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    axis = np.array(axis) / np.linalg.norm(axis)
    x, y, z = axis
    return np.array([
        [c + x*x*(1-c),   x*y*(1-c) - z*s, x*z*(1-c) + y*s, 0],
        [y*x*(1-c) + z*s, c + y*y*(1-c),   y*z*(1-c) - x*s, 0],
        [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c),   0],
        [0,               0,               0,               1]
    ])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# ЗАВДАННЯ 7: Обертання та масштабування навколо опорної точки

"""
Опорна точка (pivot): P(1, 2, 3).
Оскільки і розтяг (у 3 рази по Z), і поворот (на 30° навколо Z) відбуваються навколо ОДНІЄЇ І ТІЄЇ Ж опорної точки, можу об'єднати процес:
1. Перемістити pivot у центр: T_inv = T(-1, -2, -3)
2. Застосувати масштабування: S = S(1, 1, 3)
3. Застосувати обертання: R = Rz(30)
4. Повернути об'єкт на місце: T_pivot = T(1, 2, 3)
M = T_pivot * R * S * T_inv
"""

class Task7Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in CUBE_VERTICES for coord in v])
        self["init"] = poly_init

        T_inv = T_mat3d(-1, -2, -3)
        S = S_mat3d(1, 1, 3)
        R = R_z_mat3d(30)
        T_pivot = T_mat3d(1, 2, 3)

        M_total = T_pivot @ R @ S @ T_inv

        poly_final = SimplePolygon(color="red")
        poly_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = poly_final

        px, py, pz = 1, 2, 3
        pivot = SimplePolygon(color="black")
        pivot.set_geometry(px-0.1, py-0.1, pz, px+0.1, py+0.1, pz, px-0.1, py+0.1, pz)
        self["pivot"] = pivot

# ЗАВДАННЯ 8: Поворот навколо осі, що не проходить через центр

"""
Вісь: вектор (1, 1, 1), яка проходить через точку P(2, 3, 4).
1. Перемістити систему так, щоб P(2,3,4) стала початком: T_inv = T(-2, -3, -4)
2. Виконати обертання навколо осі (1,1,1) на 90°: R_axis
3. Повернути систему на місце: T_p = T(2, 3, 4)
4. Додаткове переміщення за умовою: T_move = T(0, -3, 2)
M = T_move * T_p * R_axis * T_inv
"""

class Task8Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # (1,2,3), (4,5,6), (7,8,9). 
        # математично ці точки лежать на одній прямій, тому візуально це буде виглядати як відрізок
        triangle_vertices = [(1,2,3), (4,5,6), (7,8,9)]

        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in triangle_vertices for coord in v])
        self["init"] = poly_init

        T_inv = T_mat3d(-2, -3, -4)
        R_axis = R_arbitrary_mat3d((1, 1, 1), 90)
        T_p = T_mat3d(2, 3, 4)
        T_move = T_mat3d(0, -3, 2)

        M_total = T_move @ T_p @ R_axis @ T_inv

        poly_final = SimplePolygon(color="green")
        poly_final.set_geometry(*apply_transformation_3d(M_total, triangle_vertices))
        self["final"] = poly_final

        px, py, pz = 2, 3, 4
        pivot = SimplePolygon(color="black")
        pivot.set_geometry(px-0.1, py-0.1, pz, px+0.1, py+0.1, pz, px-0.1, py+0.1, pz)
        self["pivot"] = pivot

# ЗАВДАННЯ 9: Зміна перспективи з використанням опорної точки

"""
Опорна точка: P(3, 3, 0).
1. Переміщення у центр: T_inv = T(-3, -3, 0)
2. Поворот на 60° навколо Y: R1 = Ry(60)
3. Поворот на 30° навколо X: R2 = Rx(30)
4. Повернення на місце: T_p = T(3, 3, 0)
M = T_p * R2 * R1 * T_inv
"""

class Task9Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        rect_vertices = [(1,2,0), (4,2,0), (4,5,0), (1,5,0)]

        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in rect_vertices for coord in v])
        self["init"] = poly_init

        T_inv = T_mat3d(-3, -3, 0)
        R1 = R_y_mat3d(60)
        R2 = R_x_mat3d(30)
        T_p = T_mat3d(3, 3, 0)

        M_total = T_p @ R2 @ R1 @ T_inv

        poly_final = SimplePolygon(color="purple")
        poly_final.set_geometry(*apply_transformation_3d(M_total, rect_vertices))
        self["final"] = poly_final

        px, py, pz = 3, 3, 0
        pivot = SimplePolygon(color="black")
        pivot.set_geometry(px-0.1, py-0.1, pz, px+0.1, py+0.1, pz, px-0.1, py+0.1, pz)
        self["pivot"] = pivot

if __name__ == '__main__':
    print("Запускаю Завдання 7...")
    Task7Scene(coordinate_rect=(-2, -2, -2, 6, 6, 12), title="Завдання 7: Pivot Scale & Rotate", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 8...")
    Task8Scene(coordinate_rect=(-2, -4, -4, 10, 10, 10), title="Завдання 8: Довільна вісь не через центр", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 9...")
    Task9Scene(coordinate_rect=(-2, -2, -2, 6, 6, 6), title="Завдання 9: Перспектива (Pivot)", grid_show=True, axis_show=True).show()