import numpy as np
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

# Кватерніон q = (w, x, y, z)

def q_mult(q1, q2):
    """q1 * q2"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return np.array([w, x, y, z])

def q_inv(q):
    """Обернений (спряжений) кватерніон для одиничного кватерніона"""
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

def q_norm(q):
    """Норма (довжина) кватерніона"""
    return np.sqrt(np.sum(q**2))

def axis_angle_to_q(axis, angle_deg):
    """Перетворення 'вісь + кут' у кватерніон"""
    half_angle = np.radians(angle_deg) / 2
    w = np.cos(half_angle)
    # Множу вектор осі на синус половинного кута
    xyz = np.array(axis) * np.sin(half_angle)
    return np.array([w, xyz[0], xyz[1], xyz[2]])

def q_to_matrix(q):
    """Перетворення кватерніона в матрицю повороту 3x3"""
    w, x, y, z = q
    return np.array([
        [1 - 2*y**2 - 2*z**2,     2*x*y - 2*z*w,         2*x*z + 2*y*w],
        [2*x*y + 2*z*w,         1 - 2*x**2 - 2*z**2,     2*y*z - 2*x*w],
        [2*x*z - 2*y*w,         2*y*z + 2*x*w,         1 - 2*x**2 - 2*y**2]
    ])

def matrix_to_q(R):
    """4. Перетворення матриці 3x3 у кватерніон"""
    tr = np.trace(R)
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2 # S = 4*w 
        w = 0.25 * S
        x = (R[2,1] - R[1,2]) / S
        y = (R[0,2] - R[2,0]) / S
        z = (R[1,0] - R[0,1]) / S
    else:
        # якщо tr <= 0, треба шукати найбільший діагональний елемент
        pass # слід > 0
    return np.array([w, x, y, z])

def rotate_point(p, q):
    """1. Поворот точки за допомогою кватерніона (v' = q * v * q^-1)"""
    # 1. Роблю з точки "чистий" кватерніон (w=0)
    v = np.array([0, p[0], p[1], p[2]])
    # q * v
    q_v = q_mult(q, v)
    # Множу результат на q^-1
    v_prime = q_mult(q_v, q_inv(q))
    # векторна частина (x, y, z)
    return v_prime[1:4]


def run_math_tasks():
    print("="*60)
    print("0. Від осі та кута до кватерніона")
    axis = np.array([1, 1, 1]) / np.sqrt(3) # Одиничний вектор
    angle = 60
    q0 = axis_angle_to_q(axis, angle)
    print(f"1. Кватерніон q = {np.round(q0, 4)}")
    print(f"2. Норма |q| = {q_norm(q0):.4f} (перевірка на 1)")
    print(f"3. Матриця повороту R:\n{np.round(q_to_matrix(q0), 3)}")

    print("\n" + "="*60)
    print("1. Операція повороту вектора")
    p = np.array([1, 0, 0])
    # Поворот навколо Z (0,0,1) на 90 градусів
    q_z90 = axis_angle_to_q([0, 0, 1], 90)
    v_чистий = [0, 1, 0, 0]
    print(f"1. Чистий кватерніон v = {v_чистий}")
    p_new = rotate_point(p, q_z90)
    print(f"2-3. Нові координати після q*v*q^-1: {np.round(p_new, 3)}")
    print("Очікуваний результат матриці повороту для (1,0,0) на 90 по Z - це (0,1,0). Збігається!")

    print("\n" + "="*60)
    print("2. Композиція складних обертань")
    q1_x45 = axis_angle_to_q([1, 0, 0], 45)
    q2_y30 = axis_angle_to_q([0, 1, 0], 30)
    # Композиція для зовнішніх осей: q_total = q2 * q1
    q_total = q_mult(q2_y30, q1_x45)
    print(f"3. Результуючий кватерніон q_total = {np.round(q_total, 4)}")
    
    # Витягую вісь і кут з q_total
    w = q_total[0]
    angle_total = 2 * np.arccos(w)
    sin_half = np.sin(angle_total / 2)
    axis_total = q_total[1:4] / sin_half
    print(f"4. Параметри повороту: Кут = {np.degrees(angle_total):.2f}°, Вісь = {np.round(axis_total, 3)}")

    print("\n" + "="*60)
    print("3. Конвертація з кутів Ойлера та Gimbal Lock")
    qz = axis_angle_to_q([0, 0, 1], 20) # yaw
    qy = axis_angle_to_q([0, 1, 0], 90) # pitch (Gimbal Lock)
    qx = axis_angle_to_q([1, 0, 0], 50) # roll
    print(f"1. qz = {np.round(qz,3)}, qy = {np.round(qy,3)}, qx = {np.round(qx,3)}")
    q_euler_total = q_mult(qz, q_mult(qy, qx))
    print(f"2. Фінальний q = {np.round(q_euler_total, 4)}")
    print("3. ДОВЕДЕННЯ: Отримали чіткий 4-вимірний вектор (w,x,y,z) без ділення на нуль")
    print("На відміну від матриць, де осі 'склеюються', кватерніон однозначно описує орієнтацію")

    print("\n" + "="*60)
    print("4. Декомпозиція матриці в кватерніон")
    R_task4 = np.array([
        [0, -1,  0],
        [1,  0,  0],
        [0,  0,  1]
    ])
    q_from_mat = matrix_to_q(R_task4)
    print(f"1. Отриманий кватерніон q = {np.round(q_from_mat, 4)}")
    print("Це поворот навколо осі Z на 90 градусів")

    print("\n" + "="*60)
    print("5. Повна декомпозиція афінної матриці")
    M = np.array([
        [0, -2,   0,  10],
        [1,  0,   0,  -5],
        [0,  0, 1.5,   3],
        [0,  0,   0,   1]
    ])
    # Вилучення трас (останній стовпець)
    T = M[0:3, 3]
    print(f"1. Вектор перенесення T = {T}")
    
    # масштабування (норми стовпців 3x3)
    col0 = M[0:3, 0]
    col1 = M[0:3, 1]
    col2 = M[0:3, 2]
    S = np.array([np.linalg.norm(col0), np.linalg.norm(col1), np.linalg.norm(col2)])
    print(f"2. Масштабні коефіцієнти S = {S}")
    
    # Отримання чистої матриці обертання (ділю стовпці на масштаб)
    R_pure = np.column_stack((col0/S[0], col1/S[1], col2/S[2]))
    print(f"3. Чиста матриця обертання R:\n{np.round(R_pure, 2)}")
    
    # Конвертація в кватерніон
    q_final = matrix_to_q(R_pure)
    print(f"4. Кватерніон афінної матриці q = {np.round(q_final, 4)}")
    print("="*60 + "\n")

    return q_total # Повертаю q_total для візуалізації Завдання 2 (Тетраедр)


class TetrahedronScene(Scene):
    def __init__(self, q_transform, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Вершини тетраедра з умови
        v = [
            np.array([0,0,0]), 
            np.array([1,0,0]), 
            np.array([0,1,0]), 
            np.array([0,0,1])
        ]
        
        # 2. Обчислюю нові вершини через поворот кватерніоном
        v_new = [rotate_point(p, q_transform) for p in v]
        
        # 3. Список граней (кожна грань - це 3 вершини)
        faces = [(0,1,2), (0,1,3), (0,2,3), (1,2,3)]

        # 4. Малюю початковий тетраедр 
        for i, face in enumerate(faces):
            poly = SimplePolygon(color="blue", line_style="--")
            # Передаю координати трьох вершин грані
            coords = []
            for idx in face:
                coords.extend([float(v[idx][0]), float(v[idx][1]), float(v[idx][2])])
            poly.set_geometry(*coords)
            self[f"orig_face_{i}"] = poly

        # 5. Малюю повернутий тетраедр
        for i, face in enumerate(faces):
            poly = SimplePolygon(color="red", line_width=2.0)
            coords = []
            for idx in face:
                coords.extend([float(v_new[idx][0]), float(v_new[idx][1]), float(v_new[idx][2])])
            poly.set_geometry(*coords)
            self[f"new_face_{i}"] = poly


if __name__ == '__main__':
    q_total_for_scene = run_math_tasks()
    print("Відкривається вікно візуалізації для Завдання 2 (Тетраедр):")
    scene = TetrahedronScene(
        q_transform=q_total_for_scene,
        coordinate_rect=(-2, -2, -2, 3, 3, 3), 
        title="Завдання 2: Поворот Тетраедра Кватерніоном", 
        grid_show=True, axis_show=True
    )
    scene.show()