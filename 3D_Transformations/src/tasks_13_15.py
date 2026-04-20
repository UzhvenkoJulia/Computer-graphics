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
    return np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

def S_mat3d(sx, sy, sz):
    return np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])

def R_x_mat3d(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

def R_y_mat3d(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

TETRAHEDRON_VERTICES = [
    (0,0,0), (1,0,0), (0,1,0), (0,0,1)
]

# ЗАВДАННЯ 13: Внутрішні обертання та локальна система координат

"""
Об'єкт: тетраедр.
Локальні (внутрішні) трансформації означають, що ми множимо матриці СПРАВА.
1. Обертання на 45° навколо локальної осі Y: M = M * Ry(45)
2. Переміщення на 2 од. вздовж локальної осі Z: M = M * Tz(2)
3. Обертання на 30° навколо локальної осі X: M = M * Rx(30)
M = Ry(45) * T(0,0,2) * Rx(30)
"""

class Task13Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in TETRAHEDRON_VERTICES for coord in v])
        self["init"] = poly_init

        M = np.eye(4)
        
        # множ СПРАВА
        M = M @ R_y_mat3d(45)
        M = M @ T_mat3d(0, 0, 2)
        M = M @ R_x_mat3d(30)

        poly_final = SimplePolygon(color="orange")
        poly_final.set_geometry(*apply_transformation_3d(M, TETRAHEDRON_VERTICES))
        self["final"] = poly_final

# ЗАВДАННЯ 15: Складна композиція та декомпозиція

"""
куб
1. Масштабування у 2 рази відносно (1,1,1): 
   M1 = T(1,1,1) * S(2,2,2) * T(-1,-1,-1)
2. Внутрішнє обертання навколо локальної Y на 90° (множимо СПРАВА): 
   M2 = M1 * Ry(90)
3. Зовнішнє переміщення на (-3, 4, 2) (множимо ЗЛІВА): 
   M3 = T(-3,4,2) * M2
"""

class Task15Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in CUBE_VERTICES for coord in v])
        self["init"] = poly_init

        # (1,1,1)
        M_scale = T_mat3d(1,1,1) @ S_mat3d(2,2,2) @ T_mat3d(-1,-1,-1)
        
        # 2. Внутрішнє обертання (СПРАВА)
        M_local = M_scale @ R_y_mat3d(90)
        
        # 3. Зовнішнє переміщення (ЗЛІВА)
        M_final = T_mat3d(-3, 4, 2) @ M_local

        poly_final = SimplePolygon(color="red")
        poly_final.set_geometry(*apply_transformation_3d(M_final, CUBE_VERTICES))
        self["final"] = poly_final

        print("\n--- ЗАВДАННЯ 15: ДЕКОМПОЗИЦІЯ ФІНАЛЬНОЇ МАТРИЦІ ---")
        
        # Витягую вектор перенесення (останній стовпець)
        translation = M_final[0:3, 3]
        
        # Витягую матрицю 3x3 (Масштаб + Обертання)
        A = M_final[0:3, 0:3]
        
        # Масштаб - це довжини стовпців матриці А
        scale_x = np.linalg.norm(A[:, 0])
        scale_y = np.linalg.norm(A[:, 1])
        scale_z = np.linalg.norm(A[:, 2])
        
        # Чиста матриця обертання
        S_inv = np.diag([1/scale_x, 1/scale_y, 1/scale_z])
        R_pure = A @ S_inv
        
        trace = np.trace(R_pure)
        angle_rad = np.arccos(np.clip((trace - 1) / 2, -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)
        
        print(f"Масштабування: Sx={scale_x:.1f}, Sy={scale_y:.1f}, Sz={scale_z:.1f}")
        print(f"Переміщення: dx={translation[0]:.1f}, dy={translation[1]:.1f}, dz={translation[2]:.1f}")
        print(f"Кут локального повороту: {angle_deg:.1f}°")
        print("---------------------------------------------------\n")

if __name__ == '__main__':
    print("Запускаю Завдання 13...")
    Task13Scene(coordinate_rect=(-4, -4, -4, 6, 6, 6), title="Завдання 13: Локальні координати", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 15...")
    Task15Scene(coordinate_rect=(-6, -2, -2, 4, 8, 8), title="Завдання 15: Складна композиція", grid_show=True, axis_show=True).show()