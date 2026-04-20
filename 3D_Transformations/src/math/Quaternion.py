import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4


class Quaternion:
    ERROR_MESSAGE_ROTATION = "Rotation vector must contain exactly 3 real elements."
    ERROR_MESSAGE_ADD = "Right operand must be a number, list or Quaternion."
    ERROR_MESSAGE_MULT = "Multiplication is only possible with other Matrix4x4 objects or numpy.ndarray 4x4."
    ERROR_MESSAGE_INV_DOESNT_EXIST = "Zero quaternion."

    def __init__(self, *a):
        """
        Quaternion initialization with copy support.
        If one argument is passed and it is another quaternion, a copy is created.
        If 4 arguments are passed, the corresponding quaternion is created.
        If no arguments are provided, the identity quaternion (1, 0, 0, 0) is created.
        If the argument is a vector v=(v.x, v.y, v.z) of type Vec3, creates quaternion v.x*i + v.y*j + v.z*k.
        If v=(v.x, v.y, v.z, v.w) of type Vec4, creates quaternion v.w + v.x*i + v.y*j + v.z*k.
        Lists, tuples and numpy arrays are also supported.
        """
        if len(a) == 1:
            if isinstance(a[0], Quaternion):
                self.q = np.array(a[0].q)
            elif isinstance(a[0], Vec4):
                v = a[0]
                self.q = np.array([v.w, v.x, v.y, v.z])
            elif isinstance(a[0], Vec3):
                v = a[0]
                self.q = np.array([0, v.x, v.y, v.z])
            elif isinstance(a[0], (list, tuple, np.ndarray)) and len(a[0]) == 4:
                self.q = np.array(a[0])
            else:
                self.q = np.array([1, 0, 0, 0])  # Identity quaternion
        elif len(a) == 4:
            self.q = np.array(a)
        else:
            self.q = np.array([1, 0, 0, 0])  # Identity quaternion

    @property
    def w(self):
        return self.q[0]

    @w.setter
    def w(self, value):
        self.q[0] = value

    @property
    def x(self):
        return self.q[1]

    @x.setter
    def x(self, value):
        self.q[1] = value

    @property
    def y(self):
        return self.q[2]

    @y.setter
    def y(self, value):
        self.q[2] = value

    @property
    def z(self):
        return self.q[3]

    @z.setter
    def z(self, value):
        self.q[3] = value

    @property
    def xyz(self):
        return self.x, self.y, self.z

    @property
    def xyzw(self):
        return self.x, self.y, self.z, self.w

    @property
    def wxyz(self):
        return self.w, self.x, self.y, self.z

    def __getitem__(self, item):
        return self.q[item]

    def __setitem__(self, key, value):
        self.q[key] = value

    def __add__(self, other):
        """Addition of two quaternions."""
        if isinstance(other, (float, int)):
            return Quaternion(self.w + other, self.x + other, self.y + other, self.z + other)
        elif isinstance(other, (Quaternion, np.ndarray, list, tuple)):
            return Quaternion(self.q + Quaternion(other).q)
        else:
            raise TypeError(Quaternion.ERROR_MESSAGE_ADD)

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return Quaternion(self.x - other, self.y - other, self.z - other, self.w - other)
        elif isinstance(other, (Quaternion, np.ndarray, list, tuple)):
            return self + (-Quaternion(other))
        else:
            raise TypeError(Quaternion.ERROR_MESSAGE_ADD)

    def __mul__(self, other):
        """Multiplication of two quaternions."""
        if isinstance(other, (float, int)):
            return Quaternion(self.q * other)

        elif isinstance(other, Quaternion):
            q0, q1, q2, q3 = self.q
            p0, p1, p2, p3 = other.q

            return Quaternion(
                q0 * p0 - q1 * p1 - q2 * p2 - q3 * p3,
                q0 * p1 + q1 * p0 + q2 * p3 - q3 * p2,
                q0 * p2 - q1 * p3 + q2 * p0 + q3 * p1,
                q0 * p3 + q1 * p2 - q2 * p1 + q3 * p0
            )

    def __len__(self):
        return 4

    def __iter__(self):
        return iter(self.q)

    def __neg__(self):
        """Declares unary minus (-obj)"""
        return Quaternion(-self.q)  # Return new object with negated value

    def __str__(self):
        """Returns the string representation of the quaternion."""
        return f"( {self.w:0.5f} + {self.x:0.5f}i + {self.y:0.5f}j + {self.z:0.5f}k )"

    def __repr__(self):
        return str(self)

    def conjugate(self):
        """Returns the conjugate quaternion."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm2(self):
        return np.dot(self.q, self.q)

    def norm(self):
        return self.norm2() ** 0.5

    def normalize(self):
        norm_squared = self.norm()
        if norm_squared == 0:
            raise ZeroDivisionError(Quaternion.ERROR_MESSAGE_INV_DOESNT_EXIST)
        self.q = self.q / float(norm_squared)

    def normalized(self):
        normalized = Quaternion(self)
        normalized.normalize()
        return normalized

    def toVec3(self):
        return Vec3(self.x, self.y, self.z)

    def toVec4(self):
        return Vec4(self.x, self.y, self.z, self.w)

    def inverse(self):
        """Returns the inverse quaternion."""
        norm_squared = np.dot(self.q, self.q)
        if norm_squared == 0:
            raise ZeroDivisionError(Quaternion.ERROR_MESSAGE_INV_DOESNT_EXIST)
        return Quaternion(self.conjugate().q / norm_squared)

    def __Q(self):
        q0, q1, q2, q3 = self.q
        return Mat4x4(
            q0, -q1, -q2, -q3,
            q1, q0, -q3, q2,
            q2, q3, q0, -q1,
            q3, -q2, q1, q0
        )

    def __Q_tilda(self):
        q0, q1, q2, q3 = self.q
        return Mat4x4(
            q0, -q1, -q2, -q3,
            q1, q0, q3, -q2,
            q2, -q3, q0, q1,
            q3, q2, -q1, q0
        )

    def toRotationMatrix(self):
        QQ = self.__Q() * self.__Q_tilda().T
        return Mat4x4(QQ[1:, 1:])

    @staticmethod
    def rotation(theta, axis):
        """Creates a quaternion for rotation by angle theta around the given axis."""
        cos_theta = np.cos(theta / 2)
        sin_theta = np.sin(theta / 2)
        if isinstance(axis, (Vec3, Vec4)):
            axis = Vec3(axis.xyz).normalized()
        elif isinstance(axis, (tuple, list, np.ndarray)) and len(axis) == 3:
            axis = Vec3(*axis).normalized()
        else:
            raise TypeError(Quaternion.ERROR_MESSAGE_ROTATION)

        return Quaternion(cos_theta, *(axis * sin_theta))

    @staticmethod
    def rotation_x(theta):
        """Creates a quaternion for rotation by angle theta around the OX axis."""
        cos_theta = np.cos(theta / 2)
        sin_theta = np.sin(theta / 2)
        axis = np.array((1, 0, 0))
        return Quaternion(cos_theta, *(axis * sin_theta))

    @staticmethod
    def rotation_y(theta):
        """Creates a quaternion for rotation by angle theta around the OY axis."""
        cos_theta = np.cos(theta / 2)
        sin_theta = np.sin(theta / 2)
        axis = np.array((0, 1, 0))
        return Quaternion(cos_theta, *(axis * sin_theta))

    @staticmethod
    def rotation_z(theta):
        """Creates a quaternion for rotation by angle theta around the OZ axis."""
        cos_theta = np.cos(theta / 2)
        sin_theta = np.sin(theta / 2)
        axis = np.array((0, 0, 1))
        return Quaternion(cos_theta, *(axis * sin_theta))

    def rotate_vector(self, u):
        """Rotates 3D vector u around axis v by angle theta using a quaternion."""
        if isinstance(u, Vec4):
            vector_quaternion = Quaternion(0, *u.xyz)
        elif isinstance(u, Vec3):
            vector_quaternion = Quaternion(u)
        elif isinstance(u, (tuple, list, np.ndarray)) and len(u) == 3:
            vector_quaternion = Quaternion(0, *u)
        else:
            vector_quaternion = Quaternion()

        rotated = self * vector_quaternion * self.conjugate()
        return Vec4(rotated.x, rotated.y, rotated.z)

    def to_angle_axis(self):
        """Computes rotation angle and axis from the quaternion"""
        w, x, y, z = self.wxyz
        angle = 2 * np.arccos(w)

        sin_half_angle = np.sqrt(1 - w * w)
        if sin_half_angle < 1e-6:
            axis = Vec3(1.0, 0.0, 0.0)  # axis is arbitrary when angle ≈ 0
        else:
            axis = Vec3(x, y, z) / sin_half_angle

        return angle, axis


if __name__ == "__main__":
    # Usage example
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)
    q3 = Quaternion(q1)  # Copy
    q4 = Quaternion()  # Identity quaternion
    q5 = Quaternion([9, 10, 11, 12])  # Initialization from list
    q6 = Quaternion(np.array([13, 14, 15, 16]))  # Initialization from numpy

    print("q1:", q1)
    print("q2:", q2)
    print("q3 (copy of q1):", q3)
    print("q4 (identity quaternion):", q4)
    print("q5 (initialized from list):", q5)
    print("q6 (initialized from numpy array):", q6)
    print("q1 + q2:", q1 + q2)
    print("q1 * q2:", q1 * q2)
    print("Conjugate of q1:", q1.conjugate())

    q7 = Quaternion(q6)
    print("||q7||^2 =  ", q7.norm2())
    print("||q7|| =  ", q7.norm())
    print()
    q7.normalize()
    print("q7:", q7)
    print("||q7||^2 =  ", q7.norm2())
    print("||q7|| =  ", q7.norm())

    q8 = Quaternion(q6)
    print("q8:", q8)
    print("q8.normalized:", q8.normalized())

    q8.z = 8888
    print("q8 (changed):", q8)

    q9 = -q8
    print("q9 (changed):", q9)

    print(*q9)

    q10 = Quaternion(2, 3, 4, 5)
    q11 = Quaternion(1, 1, 1, 1)
    q12 = q10 + q11

    print(f"{q12=}")

    q12 -= q10
    print(f"{q12=}")
    q12 += q11
    print(f"{q12=}")
    print("==========")
    print(Quaternion(1, 2, 3, 4))
    print(Quaternion(1, 2, 3, 4) - 2)
    q13 = Quaternion(1, 2, 3, 4)

    print("==========")
    q13 += 10
    print(q13)

    q14 = q13 - (1, 1, 2, 2)

    print(q14)

    print("============ 1111 ========")
    v15 = Vec3(1, 2, 3)
    q15 = Quaternion(v15)
    print(v15)
    print(q15)

    print("++++++++++++++++")
    print(q14)
    print(q14.toVec4())
    print(q14.toVec3())

    print("=========")
    q16 = Quaternion(1, 2, 3, 4)
    q17 = q16 * 2
    print(q16)
    print(q17)
    q16 *= 2
    print(q16)
