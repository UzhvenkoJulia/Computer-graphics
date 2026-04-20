import numpy as np
import random
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

# 3D

def apply_transformation_3d(matrix, points):
    """Множить 3D точки (x, y, z, 1) на матрицю 4x4"""
    result_coords = []
    for p in points:
        vec = np.array([p[0], p[1], p[2], 1])
        new_vec = matrix.dot(vec)
        # x, y, z як плоский список
        result_coords.extend([float(new_vec[0]), float(new_vec[1]), float(new_vec[2])])
    return result_coords

def T_mat3d(dx, dy, dz):
    """матриця переміщення у 3D"""
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def R_x_mat3d(angle):
    """матриця повороту навколо осі X"""
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])

def R_y_mat3d(angle):
    """Y"""
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ])

def R_z_mat3d(angle):
    """Z"""
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])

def R_arbitrary_mat3d(axis, angle_deg):
    """навколо довільної осі"""
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    
    axis = np.array(axis) / np.linalg.norm(axis)
    ux, uy, uz = axis
    
    return np.array([
        [c + ux**2 * (1 - c),       ux * uy * (1 - c) - uz * s, ux * uz * (1 - c) + uy * s, 0],
        [uy * ux * (1 - c) + uz * s, c + uy**2 * (1 - c),       uy * uz * (1 - c) - ux * s, 0],
        [uz * ux * (1 - c) - uy * s, uz * uy * (1 - c) + ux * s, c + uz**2 * (1 - c),       0],
        [0,                          0,                          0,                        1]
    ])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0), 
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)  
]

# тетраедр (в початку координат)
TETRAHEDRON_VERTICES = [
    (0,0,0), (1,0,0), (0,1,0), (0,0,1)
]

# ЗАВДАННЯ 4: Композиція трансформацій у 3D (EulerAngles)

"""
Потрібно послідовно застосувати дві трансформації до куба.
Це означає, що множу їхні матриці 4x4.

1.  **Поворот на кути Ейлера (20°, 35°, 50°) у системі ZYX:**
    Це означає послідовне множення матриць: R = Rz(20) * Ry(35) * Rx(50).
    * Rz(20): Поворот навколо Z.
    * Ry(35): Поворот навколо Y.
    * Rx(50): Поворот навколо X.

    Результуюча матриця повороту R (після множення) буде приблизно:
    R ≈ | 0.770   0.194   0.609   0 |
        | 0.280   0.754  -0.594   0 |
        |-0.574   0.627   0.527   0 |
        | 0       0       0       1 |

2.  **Переміщення на вектор (1, 3, -2):**
    Матриця T_move:
    T ≈ | 1  0  0   1 |
        | 0  1  0   3 |
        | 0  0  1  -2 |
        | 0  0  0   1 |

3.  **Повна композиція трансформацій (М_total):**
    Оскільки переміщення застосовується ПІСЛЯ повороту, множу: M = T_move * R.
    M ≈ | 0.770   0.194   0.609   1 |
        | 0.280   0.754  -0.594   3 |
        |-0.574   0.627   0.527  -2 |
        | 0       0       0       1 |
"""

class Task4Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        # список вершин у плоский список координат для set_geometry
        poly_init.set_geometry(*[coord for vertex in CUBE_VERTICES for coord in vertex])
        self["init"] = poly_init

        R = R_z_mat3d(20) @ R_y_mat3d(35) @ R_x_mat3d(50)
        
        T_move = T_mat3d(1, 3, -2)

        M_total = T_move @ R

        poly_final = SimplePolygon(color="red")
        poly_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = poly_final

# ЗАВДАННЯ 5: Рандомізована композиція на тетраедрі

"""
Оскільки це рандом, не можу я заздалегідь розрахувати матриці.
Їх створюватиме Python під час кожного запуску.

1.  **Генерація випадкових параметрів (random library):**
    * Кут обертання: float від 10° до 90°.
    * Вісь обертання: вектор (ux, uy, uz), де кожна компонента — random_uniform від -1 до 1.
    * Вектор переміщення: вектор (tx, ty, tz), де компоненти — random_uniform від -5 до 5.

2.  **Побудова матриць (4x4):**
    * Матриця R: Створюється на основі випадкової осі та випадкового кута (функція R_arbitrary_mat3d).
    * Матриця T: Створюється на основі випадкового вектора переміщення (функція T_mat3d).

3.  **Композиція трансформацій (М_total):**
    M = T * R.
"""

class Task5Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for vertex in TETRAHEDRON_VERTICES for coord in vertex])
        self["init"] = poly_init

        angle = random.uniform(10, 90)
        axis = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        tx, ty, tz = random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)

        print(f"Завдання 5 Рандом: Кут={angle:.1f}°, Вісь={axis}, Зсув=({tx:.1f}, {ty:.1f}, {tz:.1f})")

        R = R_arbitrary_mat3d(axis, angle)
        T = T_mat3d(tx, ty, tz)
        M_total = T @ R

        poly_final = SimplePolygon(color="orange")
        poly_final.set_geometry(*apply_transformation_3d(M_total, TETRAHEDRON_VERTICES))
        self["final"] = poly_final

# ЗАВДАННЯ 6: Обертання куба навколо опорної точки (Pivot)

"""
Опорна точка (pivot point): (2, 0, 3).
Потрібно обернути куб навколо цієї точки на 45° навколо осі Y.
А потім перемістити його.

1.  **Обертання з опорною точкою (T_pivot):**
    Виконується у три кроки:
    * а) Переміщення в початок координат: T1 = T(-2, 0, -3).
    * б) Виконати обертання Ry(45): R1 = Ry(45).
    * в) Повернути назад: T2 = T(2, 0, 3).
    M_pivot = T2 * R1 * T1.

2.  **Фінальне переміщення на вектор (-1, 2, 4):**
    T_move:
    T3 = T(-1, 2, 4).

3.  **Повна композиція трансформацій (М_total):**
    Фінальне переміщення ПІСЛЯ обертання: M = T3 * M_pivot.
    M_total = T(-1, 2, 4) * T(2, 0, 3) * Ry(45) * T(-2, 0, -3).
"""

class Task6Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for vertex in CUBE_VERTICES for coord in vertex])
        self["init"] = poly_init

        px, py, pz = 2, 0, 3
        angle = 45

        # Обертання навколо Pivot (PivotMatrix)
        T1 = T_mat3d(-px, -py, -pz) 
        R1 = R_y_mat3d(angle)  # Обертання Ry(45)
        T2 = T_mat3d(px, py, pz)  
        
        M_pivot = T2 @ R1 @ T1

        T3 = T_mat3d(-1, 2, 4)  # (-1, 2, 4)
        M_total = T3 @ M_pivot

        poly_final = SimplePolygon(color="green")
        poly_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = poly_final

        pivot = SimplePolygon(color="black")
        pivot.set_geometry(px-0.1, py-0.1, pz, px+0.1, py+0.1, pz, px-0.1, py+0.1, pz)
        self["pivot"] = pivot

if __name__ == '__main__':
    # coordinate_rect задає 3D простір візуалізації
    
    print("Запускаю Завдання 4...")
    Task4Scene(
        coordinate_rect=(-2, -1, -3, 5, 5, 5), # (xmin, ymin, zmin, xmax, ymax, zmax)
        title="Завдання 4: EulerAngles ZYX order", 
        grid_show=True, axis_show=True
    ).show()
    
    print("Запускаю Завдання 5...")
    Task5Scene(
        coordinate_rect=(-6, -6, -6, 6, 6, 6),
        title="Завдання 5: Рандомізація",
        grid_show=True, axis_show=True
    ).show()
    
    print("Запускаю Завдання 6...")
    Task6Scene(
        coordinate_rect=(-4, -4, -4, 8, 8, 8),
        title="Завдання 6: Pivot Point (2, 0, 3)",
        grid_show=True, axis_show=True
    ).show()