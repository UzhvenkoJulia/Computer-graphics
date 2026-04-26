# Завдання 3: різниця між конвенціями XYZ та ZYX (зовнішні осі)
# Головне правило матричної алгебри: порядок множення має значення (A * B != B * A).
#
# 1. Конвенція XYZ (зовнішні осі): 
#    Спочатку кручу навколо X, потім навколо глобальної Y, потім навколо глобальної Z
#    Математично це записується з кінця на початок: R_XYZ = Rz * Ry * Rx
#
# 2. Конвенція ZYX (зовнішні осі): 
#    Спочатку Z, потім Y, потім X
#    R_ZYX = Rx * Ry * Rz
#
# Оскільки порядок множення різний, кінцеві координати вершин куба 
# будуть знаходитися в абсолютно різних місцях простору!



import numpy as np
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

# 3D
def apply_transformation_3d(matrix, points):
    """Множить точки куба на матрицю трансформації 4x4"""
    result_coords = []
    for p in points:
        vec = np.array([p[0], p[1], p[2], 1]) # у однорідних координатах
        new_vec = matrix.dot(vec)
        result_coords.extend([float(new_vec[0]), float(new_vec[1]), float(new_vec[2])])
    return result_coords

def T_mat(dx, dy, dz):
    """Матриця переміщення"""
    return np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

def S_mat(sx, sy, sz):
    """Матриця розтягу/стиснення"""
    return np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])

def Rx(angle):
    """Обертання навколо осі X"""
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

def Ry(angle):
    """Обертання навколо осі Y"""
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

def Rz(angle):
    """Обертання навколо осі Z"""
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# 1: Розтяг, обертання (Euler XYZ) і зсув
class Task1Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Початковий куб (синій, пунктир)
        cube_init = SimplePolygon(color="blue", line_style="--")
        cube_init.set_geometry(*[c for p in CUBE_VERTICES for c in p])
        self["init"] = cube_init

        # 2. Будую матриці за умовою
        # Крок 1: Розтяг X=2, Y=0.5, Z=1 (Z не вказано, отже 1)
        S = S_mat(2, 0.5, 1)
        
        # Крок 2: Обертання Euler XYZ (30, 45, 60)
        # Для зовнішніх осей множу Rz * Ry * Rx
        R = Rz(60) @ Ry(45) @ Rx(30)
        
        # Крок 3: Переміщення (-3, 2, 5)
        T = T_mat(-3, 2, 5)

        # Результуюча матриця: Переміщення застосовується останнім (зліва)
        M_total = T @ R @ S

        print("\nЗАВДАННЯ 1: МАТРИЦІ\ї")
        print("Матриця розтягу S:\n", np.round(S, 2))
        print("Матриця обертання R (XYZ):\n", np.round(R, 2))
        print("Матриця переміщення T:\n", np.round(T, 2))
        print("Результуюча M_total:\n", np.round(M_total, 2))

        # 4. Фінальний куб (червоний)
        cube_final = SimplePolygon(color="red")
        cube_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = cube_final

# 2: Поворот у системі кутів Ейлера (ZYX)
class Task2Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        cube_init = SimplePolygon(color="blue", line_style="--")
        cube_init.set_geometry(*[c for p in CUBE_VERTICES for c in p])
        self["init"] = cube_init

        # Крок 1: Обертання ZYX (20, 35, 50)
        # Rx * Ry * Rz
        R = Rx(50) @ Ry(35) @ Rz(20)
        
        # Крок 2: Переміщення (1, 3, -2)
        T = T_mat(1, 3, -2)

        M_total = T @ R

        print("\nЗАВДАННЯ 2: МАТРИЦІ")
        print("Матриця обертання R (ZYX):\n", np.round(R, 2))
        print("Результуюча M_total:\n", np.round(M_total, 2))

        cube_final = SimplePolygon(color="green")
        cube_final.set_geometry(*apply_transformation_3d(M_total, CUBE_VERTICES))
        self["final"] = cube_final

# 3: Конвенції та послідовність обертань (Аналітика)
def run_task_3():
    print("\n" + "="*50)
    print("ЗАВДАННЯ 3: ПОРІВНЯННЯ КОНВЕНЦІЙ")
    
    # Кути a=45, b=30, y=60
    a, b, y = 45, 30, 60
    
    # 1. Конвенція XYZ (зовнішні), Rz * Ry * Rx
    R_xyz = Rz(y) @ Ry(b) @ Rx(a)
    
    # 2. Конвенція ZYX (зовнішні), Rx * Ry * Rz
    R_zyx = Rx(a) @ Ry(b) @ Rz(y)

    print("Матриця R для конвенції XYZ (зовнішні):")
    print(np.round(R_xyz, 3))
    
    print("\nМатриця R для конвенції ZYX (зовнішні):")
    print(np.round(R_zyx, 3))

    print("\nВИСНОВОК:")
    print("Матриці абсолютно різні. Це відбувається тому, що множення матриць ")
    print("не є комутативним (A * B != B * A). Порядок застосування осей змінює")
    print("орієнтацію локальної системи координат об'єкта в просторі")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_task_3()
    
    print("Візуалізація Завдання 1 (Закрийте вікно, щоб перейти до наступного)...")
    Task1Scene(
        coordinate_rect=(-4, -2, -2, 4, 8, 8), 
        title="Завдання 1: S -> R(XYZ) -> T", 
        grid_show=True, axis_show=True
    ).show()
    
    print("Візуалізація Завдання 2...")
    Task2Scene(
        coordinate_rect=(-2, -2, -4, 4, 6, 2), 
        title="Завдання 2: R(ZYX) -> T", 
        grid_show=True, axis_show=True
    ).show()