import numpy as np


class Vec3:
    ERROR_MESSAGE_CONSTRUCTOR = "Непідтриманий тип даних для ініціалізації або недостатньо елементів для побудови Vec3."
    ERROR_MESSAGE_ADD = "Правий операнд має бути число, список або Vec3."
    ERROR_MESSAGE_MULT = "Правий операнд має бути число, список або Vec3."
    ERROR_MESSAGE_CROSS = "Потрібен Vec3 або список із 3 елементів."
    ERROR_MESSAGE_DIV = "Правий операнд має бути число"

    def __init__(self, *data):
        """
        Конструктор класу Vector3.
        Якщо дані не передані, створює нульовий вектор.
        Приймає:
        - список або масив із трьох елементів,
        - інший об'єкт Vector3.
        """
        if len(data) == 0:
            self.data = np.zeros(3, dtype=float)
        elif len(data) == 3:
            self.data = np.array((data), dtype=float)
        elif len(data) == 2:
            self.data = np.array((*data, 0.0), dtype=float)
        elif len(data) == 1:
            data = data[0]
            if isinstance(data, Vec3):
                self.data = np.copy(data.data)
            elif isinstance(data, (list, tuple, np.ndarray)):
                data = np.array(data)
                if data.shape == (3,):
                    data = data.astype(float)
                    self.data = np.array(data)
                else:
                    raise ValueError(Vec3.ERROR_MESSAGE_CONSTRUCTOR)
            else:
                raise ValueError(Vec3.ERROR_MESSAGE_CONSTRUCTOR)
        else:
            raise ValueError(Vec3.ERROR_MESSAGE_CONSTRUCTOR)

    def __getitem__(self, index):
        """
        Отримання елемента вектора по індексу.
        """
        return self.data[index]

    def __setitem__(self, index, value):
        """
        Встановлення значення елемента вектора по індексу.
        """
        self.data[index] = value

    def __len__(self):
        return 3

    def __str__(self):
        """
        Повертає строкове представлення вектора.
        """
        return np.array2string(self.data, formatter={'float_kind': lambda x: f"{x:8.3f}"})

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, (Vec3, np.ndarray, list, tuple)):
            return Vec3(self.data + Vec3(other).data)
        else:
            raise TypeError(Vec3.ERROR_MESSAGE_ADD)

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x - other, self.y - other, self.z - other)
        elif isinstance(other, (Vec3, np.ndarray, list, tuple)):
            return self + (-Vec3(other))
        else:
            raise TypeError(Vec3.ERROR_MESSAGE_ADD)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, (Vec3, np.ndarray, tuple, list)):
            return np.dot(self.data, Vec3(other).data)
        else:
            raise TypeError(Vec3.ERROR_MESSAGE_MULT)

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(Vec3.ERROR_MESSAGE_DIV)

    def __iter__(self):
        """Оператор *obj працює через цей метод"""
        return iter(self.data)  # Повертаємо ітератор списку

    def __neg__(self):
        return Vec3(-self.data)

    def norm2(self):
        return self * self

    def norm(self):
        return self.norm2() ** 0.5

    def normalize(self):
        n = self.norm()
        if n != 0:
            self.data = self.data / n
        else:
            return Vec3()

    def normalized(self):
        normalized = Vec3(self)
        normalized.normalize()
        return normalized

    def cross(self, other):
        """
        Обчислює векторний добуток з іншим вектором Vector3 або numpy.ndarray з 3 елементів.
        """
        if isinstance(other, (Vec3, np.ndarray, tuple, list)) and len(other) == 3:
            other = Vec3(other)
            return Vec3(np.cross(self.data, other.data))

        raise TypeError(Vec3.ERROR_MESSAGE_CROSS)

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, value):
        self.data[2] = value

    @property
    def xy(self):
        return self.data[:2]

    @property
    def xz(self):
        return np.array((self.data[0], self.data[2]))

    @property
    def yz(self):
        return np.array((self.data[1], self.data[2]))

    @property
    def xyz(self):
        return self.data[:3]

def vertex(x=0, y=0, z=1):
    return Vec3(x, y, z)


if __name__ == '__main__':
    v1 = Vec3()
    # print(v1)

    v3 = Vec3([1, 2, 3])
    print(v3)

    v1 += 4
    print(v1)
    # print(v1 + (1, 2, 4))
    # print(v1 - (1, 2, 5))

    # v = Vec3(2, 1, 4)
    # print(v)
    # print(v.norm2())
    # print(v.norm())
