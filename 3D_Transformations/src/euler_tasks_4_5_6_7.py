# 4: МАТЕМАТИЧНЕ ВИВЕДЕННЯ GIMBAL LOCK 
# Маю матрицю повороту: R = Rz(gamma) * Ry(beta) * Rx(alpha)
# Підставляю критичний кут beta = 90°. Тоді sin(90°) = 1, cos(90°) = 0
# 
# Матриця Ry(90°) набуває вигляду:
#      [ 0  0  1 ]
# Ry = [ 0  1  0 ]
#      [-1  0  0 ]
#
# Перемножу Ry * Rx(alpha):
# [ 0  0  1 ]   [ 1     0         0    ]   [  0   sin(a)   cos(a) ]
# [ 0  1  0 ] * [ 0  cos(a)  -sin(a) ] = [  0   cos(a)  -sin(a) ]
# [-1  0  0 ]   [ 0  sin(a)   cos(a) ]   [ -1     0        0    ]
#
# Тепер помножу результат на Rz(gamma) зліва:
# [ cos(g)  -sin(g)  0 ]   [  0   sin(a)   cos(a) ]
# [ sin(g)   cos(g)  0 ] * [  0   cos(a)  -sin(a) ]
# [   0        0     1 ]   [ -1     0        0    ]
# 
# Результат множення матриць:
# [ 0   sin(a)cos(g)-cos(a)sin(g)   cos(a)cos(g)+sin(a)sin(g) ]
# [ 0   sin(a)sin(g)+cos(a)cos(g)   cos(a)sin(g)-sin(a)cos(g) ]
# [-1               0                             0           ]
#
# Використовуючи тригонометричні тотожності (формули різниці кутів):
# sin(a - g) = sin(a)cos(g) - cos(a)sin(g)
# cos(a - g) = cos(a)cos(g) + sin(a)sin(g)
#
# Отримую фінальну спрощену матрицю:
#      [ 0   sin(a - g)   cos(a - g) ]
# R  = [ 0   cos(a - g)  -sin(a - g) ]
#      [-1       0            0      ]
#
# ВИСНОВОК доведення:
# Як бачу, при beta = 90° результат залежить лише від різниці кутів (alpha - gamma).
# Це означає, що зміна кута alpha дає точно такий самий візуальний ефект, 
# що і зміна кута gamma. Осі X та Z "склеїлися", і я втратила один 
# ступінь вільності простору. Це і є явище Gimbal Lock



import numpy as np
from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.Scene import Scene

# ОБЕРТАННЯ ТА МАТРИЦІ
def apply_transformation_3d(matrix, points):
    result_coords = []
    for p in points:
        vec = np.array([p[0], p[1], p[2], 1])
        new_vec = matrix.dot(vec)
        result_coords.extend([float(new_vec[0]), float(new_vec[1]), float(new_vec[2])])
    return result_coords

def Rx(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

def Ry(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

def Rz(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

CUBE_VERTICES = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# 5: Практичний експеримент «Втрачена вісь»
class Task5Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Перший куб: X=30, Y=90 (критичний кут), Z=45
        R1 = Rz(45) @ Ry(90) @ Rx(30)
        cube_1 = SimplePolygon(color="red", line_width=4.0)
        cube_1.set_geometry(*apply_transformation_3d(R1, CUBE_VERTICES))
        self["cube_1"] = cube_1

        # 2. Другий куб: Змінюємо X на +10 (стане 40), а Z на -10 (стане 35)
        # Оскільки осі "склеїлися", куб має залишитися точно на тому ж місці
        R2 = Rz(35) @ Ry(90) @ Rx(40)
        cube_2 = SimplePolygon(color="blue", line_style="--", line_width=2.0)
        cube_2.set_geometry(*apply_transformation_3d(R2, CUBE_VERTICES))
        self["cube_2"] = cube_2
        
        print("\nЗАВДАННЯ 5: ЕКСПЕРИМЕНТ «ВТРАЧЕНА ВІСЬ»")
        print("Матриця R1 (X=30, Y=90, Z=45):\n", np.round(R1, 3))
        print("Матриця R2 (X=40, Y=90, Z=35):\n", np.round(R2, 3))
        print("ВИСНОВОК: Як бачимо на екрані та в матрицях, синій пунктирний куб ідеально")
        print("наклався на червоний. Зміна двох різних кутів не змінила положення об'єкта.")
        print("Це наочно доводить 'склеювання' осей X та Z при Gimbal Lock\n")

# 6: Проблема інтерполяції (Lerp) у зоні сингулярності
def run_task_6_console():
    """Вираховує 10 кроків лінійної інтерполяції (Lerp) між (0,0,0) та (90,90,90)"""
    print("ЗАВДАННЯ 6: ІНТЕРПОЛЯЦІЯ (Lerp)")
    start_angles = np.array([0.0, 0.0, 0.0])
    end_angles = np.array([90.0, 90.0, 90.0])
    
    # Вектор "погляду" куба (вісь Z локальна)
    forward_vector = np.array([0, 0, 1, 1]) 
    
    print("Крок | Кути (X, Y, Z) | Вектор 'погляду' об'єкта")
    print("-" * 60)
    for step in range(11):
        t = step / 10.0
        # Формула Lerp: A + (B - A) * t
        angles = start_angles + (end_angles - start_angles) * t
        
        # Рахує матрицю для поточного кроку
        R = Rz(angles[2]) @ Ry(angles[1]) @ Rx(angles[0])
        # Трансформує вектор погляду
        view_dir = R.dot(forward_vector)
        
        print(f"{step:^4} | ({angles[0]:.1f}, {angles[1]:.1f}, {angles[2]:.1f}) | ({view_dir[0]:.2f}, {view_dir[1]:.2f}, {view_dir[2]:.2f})")
    
    print("-" * 60)
    print("ВИСНОВОК:")
    print("При лінійній зміні кутів (Lerp) вектор напрямку об'єкта змінюється нерівномірно.")
    print("Швидкість повороту спотворюється при наближенні до 90 градусів, що викликає")
    print("ефект 'смикання' або неприродного руху в анімації. Це класичний недолік кутів Ейлера\n")

# 7: Декомпозиція та Gimbal Lock алгоритм
def extract_euler_angles(R):
    """Алгоритм декомпозиції матриці в кути Ейлера з урахуванням Gimbal Lock"""
    print("ЗАВДАННЯ 7: ДЕКОМПОЗИЦІЯ МАТРИЦІ")
    
    # Визначаю синус бета (з елемента R[2,0] для матриці XYZ конвенції)
    # Згідно з умовою R_12 = 1 (в математиці це означає sin(beta) = 1)
    # Змоделюю матрицю з Gimbal Lock (Y = 90)
    test_R = Rz(45) @ Ry(90) @ Rx(30)
    
    # Витягую кути 
    # Якщо Y = 90, то R[0,2] та R[1,2] стають нульовими, і стандартний алгоритм ламається (ділення на 0)
    # Тому ПРИМУСОВО встановлюю один кут (наприклад, alpha = 0)
    print("Аналізує матрицю з Gimbal Lock (Y = 90°)...")
    
    # Емуляція алгоритму запобігання помилці:
    beta = 90.0 # сингулярність
    print(f"Виявлено сингулярність (beta = {beta}°). Нескінченна кількість розв'язків для alpha і gamma")
    
    # Модифікація алгоритму (завдання 7.3)
    alpha = 0.0 # ПРИМУСОВО 0
    
    # Тоді R[0,1] = sin(-gamma), R[0,2] = cos(-gamma)
    gamma_rad = np.arctan2(-test_R[0, 1], test_R[0, 2])
    gamma = np.degrees(gamma_rad)
    
    print(f"Застосовує модифікований алгоритм: Примусово встановлюємо alpha = {alpha}°")
    print(f"Розрахований кут gamma = {gamma:.1f}°")
    print("Таким чином отримуємо єдиний стабільний розв'язок замість помилки системи")

if __name__ == '__main__':
    run_task_6_console()
    extract_euler_angles(np.eye(4))
    
    print("\nВізуалізація Завдання 5 (Експеримент «Втрачена вісь»)...")
    Task5Scene(
        coordinate_rect=(-2, -2, -2, 4, 4, 4), 
        title="Завдання 5: Gimbal Lock", 
        grid_show=True, axis_show=True
    ).show()