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

def R_z_mat3d(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# ЗАВДАННЯ 10: Комплексна трансформація (з опорною точкою)

"""
1. Масштабування (Sx=2) та поворот (Ry=45) відносно опорної точки (1,1,1).
2. Переміщення на вектор (-3, 4, 2).
M = T(-3,4,2) * [ T(1,1,1) * Ry(45) * Sx(2) * T(-1,-1,-1) ]
"""

class Task10Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in CUBE_VERTICES for coord in v])
        self["init"] = poly_init

        # Трансформації навколо опорної точки
        T_inv = T_mat3d(-1, -1, -1)
        S = S_mat3d(2, 1, 1)
        R = R_y_mat3d(45)
        T_pivot = T_mat3d(1, 1, 1)
        
        T_final = T_mat3d(-3, 4, 2)

        # Композиція
        M_total = T_final @ T_pivot @ R @ S @ T_inv

        poly_final = SimplePolygon(color="red")
        poly_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = poly_final

        # Опорна точка
        px, py, pz = 1, 1, 1
        pivot = SimplePolygon(color="black")
        pivot.set_geometry(px-0.1, py-0.1, pz, px+0.1, py+0.1, pz, px-0.1, py+0.1, pz)
        self["pivot"] = pivot

# ЗАВДАННЯ 11: Порівняння зовнішніх та внутрішніх обертань

"""
Трансформація А (Зовнішні осі): X(30), Y(45), Z(60).
Зовнішні обертання множаться ЗЛІВА: M_A = Rz(60) * Ry(45) * Rx(30).

Трансформація Б (Внутрішні/Локальні осі): Z(60), Y(45), X(30).
Внутрішні обертання множаться СПРАВА: M_B = Rz(60) * Ry(45) * Rx(30).
Матриці математично ідентичні! Кубики повністю співпадуть
"""

class Task11Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="black", line_style="--")
        poly_init.set_geometry(*[coord for v in CUBE_VERTICES for coord in v])
        self["init"] = poly_init

        # Зовнішні обертання (pre-multiplication)
        M_A = R_z_mat3d(60) @ R_y_mat3d(45) @ R_x_mat3d(30)
        
        # Внутрішні обертання (post-multiplication) - порядок кутів зворотній за умовою
        M_B = R_z_mat3d(60) @ R_y_mat3d(45) @ R_x_mat3d(30)

        print("\n--- ЗАВДАННЯ 11: ДОВЕДЕННЯ ---")
        print("Матриця A (Зовнішня) дорівнює Матриці B (Внутрішня):", np.allclose(M_A, M_B))

        poly_A = SimplePolygon(color="red", line_width=4.0)
        poly_A.set_geometry(*apply_transformation_3d(M_A, CUBE_VERTICES))
        self["poly_A"] = poly_A

        # Куб Б (тонший - щоб показати, що він лежить рівно всередині червоного)
        poly_B = SimplePolygon(color="blue", line_style="--", line_width=2.0)
        poly_B.set_geometry(*apply_transformation_3d(M_B, CUBE_VERTICES))
        self["poly_B"] = poly_B

# ЗАВДАННЯ 12: Декомпозиція афінної матриці («Чорна скринька»)

"""
Нехай маю "невідому" матрицю М, яка містить Scale, Rotate і Translate.
1. Вектор перенесення = M[0:3, 3] (останній стовпець).
2. Лінійна частина (3x3) A = Scale * Rotate.
3. Коефіцієнти масштабу sx, sy, sz - це довжини стовпців матриці A.
4. Чиста матриця обертання R = A / Scale.
5. Кут: arccos((Trace(R) - 1) / 2).
6. Вісь: З антисиметричної матриці (R - R.T).
"""

class Task12Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        poly_init = SimplePolygon(color="blue", line_style="--")
        poly_init.set_geometry(*[coord for v in CUBE_VERTICES for coord in v])
        self["init"] = poly_init

        # "чорна скриньку" (довільна складна трансформація)
        # S(2, 1.5, 1) -> Rz(30) -> Ry(45) -> T(3, -2, 1)
        M = T_mat3d(3, -2, 1) @ R_z_mat3d(30) @ R_y_mat3d(45) @ S_mat3d(2, 1.5, 1)

        # перенесення
        t_vec = M[0:3, 3]
        
        # масштаб
        A = M[0:3, 0:3]
        sx = np.linalg.norm(A[:, 0])
        sy = np.linalg.norm(A[:, 1])
        sz = np.linalg.norm(A[:, 2])
        
        # матриця обертання
        S_inv = np.diag([1/sx, 1/sy, 1/sz])
        R_pure = A @ S_inv
        
        # ортогональність (R * R^T = I)
        is_orthogonal = np.allclose(R_pure @ R_pure.T, np.eye(3))

        # кут і вісь
        trace = np.trace(R_pure)
        angle_rad = np.arccos(np.clip((trace - 1) / 2, -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)
        
        sin_t = np.sin(angle_rad)
        if sin_t > 1e-6:
            R_anti = (R_pure - R_pure.T) / (2 * sin_t)
            axis = np.array([R_anti[2, 1], R_anti[0, 2], R_anti[1, 0]])
            axis = axis / np.linalg.norm(axis)
        else:
            axis = np.array([0, 0, 0])

        print("\n--- ЗАВДАННЯ 12: РЕЗУЛЬТАТИ ДЕКОМПОЗИЦІЇ ---")
        print(f"1. Перенесення: dx={t_vec[0]:.2f}, dy={t_vec[1]:.2f}, dz={t_vec[2]:.2f}")
        print(f"2. Масштабування: sx={sx:.2f}, sy={sy:.2f}, sz={sz:.2f}")
        print(f"3. Матриця обертання ортогональна? -> {is_orthogonal}")
        print(f"4. Кут повороту: {angle_deg:.2f}°")
        print(f"5. Вісь повороту: ({axis[0]:.2f}, {axis[1]:.2f}, {axis[2]:.2f})\n")

        poly_final = SimplePolygon(color="green")
        poly_final.set_geometry(*apply_transformation_3d(M, CUBE_VERTICES))
        self["final"] = poly_final

if __name__ == '__main__':
    print("Запускаю Завдання 10...")
    Task10Scene(coordinate_rect=(-4, -2, -2, 4, 6, 4), title="Завдання 10: Комплексна трансформація", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 11...")
    Task11Scene(coordinate_rect=(-2, -2, -2, 4, 4, 4), title="Завдання 11: Зовнішні vs Внутрішні", grid_show=True, axis_show=True).show()
    
    print("Запускаю Завдання 12...")
    Task12Scene(coordinate_rect=(-2, -3, -2, 6, 6, 6), title="Завдання 12: Чорна скринька", grid_show=True, axis_show=True).show()