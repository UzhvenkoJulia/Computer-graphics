import numpy as np
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

# 3D МАТРИЦІ 4x4

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

def R_arbitrary(axis, angle_deg):
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

def R_euler(rot_x, rot_y, rot_z):
    rad_x, rad_y, rad_z = np.radians(rot_x), np.radians(rot_y), np.radians(rot_z)
    Rx = np.array([[1, 0, 0, 0], [0, np.cos(rad_x), -np.sin(rad_x), 0], [0, np.sin(rad_x), np.cos(rad_x), 0], [0, 0, 0, 1]])
    Ry = np.array([[np.cos(rad_y), 0, np.sin(rad_y), 0], [0, 1, 0, 0], [-np.sin(rad_y), 0, np.cos(rad_y), 0], [0, 0, 0, 1]])
    Rz = np.array([[np.cos(rad_z), -np.sin(rad_z), 0, 0], [np.sin(rad_z), np.cos(rad_z), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return Rz @ Ry @ Rx 

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# ЗАВДАННЯ 1: Композиція трансформацій у 3D

class Task1Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cube_init = SimplePolygon(color="blue", line_style="--")
        cube_init.set_geometry(*[c for p in CUBE_VERTICES for c in p])
        self["init"] = cube_init

        R = R_arbitrary((1, 1, 0), 45)
        T = T_mat3d(2, -1, 3)
        M_total = T @ R

        cube_final = SimplePolygon(color="red")
        cube_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = cube_final

# ЗАВДАННЯ 2: Розтяг, обертання (Euler) і зсув

class Task2Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cube_init = SimplePolygon(color="blue", line_style="--")
        cube_init.set_geometry(*[c for p in CUBE_VERTICES for c in p])
        self["init"] = cube_init

        S = S_mat3d(2, 0.5, 1)
        R = R_euler(30, 45, 60)
        T = T_mat3d(-3, 2, 5)
        M_total = T @ R @ S

        cube_final = SimplePolygon(color="green")
        cube_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = cube_final

# ЗАВДАННЯ 3: Обертання навколо довільної осі

class Task3Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cube_init = SimplePolygon(color="blue", line_style="--")
        cube_init.set_geometry(*[c for p in CUBE_VERTICES for c in p])
        self["init"] = cube_init

        R_z = R_arbitrary((0, 0, 1), 60)
        R_diag = R_arbitrary((1, 1, 1), 45)
        T = T_mat3d(4, -2, 1)
        M_total = T @ R_diag @ R_z

        cube_final = SimplePolygon(color="purple")
        cube_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = cube_final

if __name__ == '__main__':
    print("Запускаю Завдання 1...")
    Task1Scene(coordinate_rect=(-2, -2, -2, 6, 6, 6), title="Завдання 1", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 2...")
    Task2Scene(coordinate_rect=(-5, -2, -2, 5, 5, 8), title="Завдання 2", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 3...")
    Task3Scene(coordinate_rect=(-2, -3, -2, 6, 6, 6), title="Завдання 3", grid_show=True, axis_show=True).show()