import numpy as np

from src.math.Rotations import rotation_matrix_x, rotation_matrix_y, rotation_matrix_z
from src.math.Scale import scale_matrix
from src.math.Translation import translation_matrix2d
from src.math.Vec3 import Vec3


class Mat3x3:
    ERROR_MESSAGE_CONSTRUCTOR = "Unsupported data type or insufficient elements to build a 3x3 matrix."
    ERROR_MESSAGE_ADD = "Addition is only possible with other Matrix3x3 objects or numpy.ndarray 3x3."
    ERROR_MESSAGE_MULT = "Multiplication is only possible with other Matrix3x3 objects or numpy.ndarray 3x3 or Vec3."
    ERROR_MESSAGE_INV_DOESNT_EXIST = "Matrix has no inverse."
    ERROR_MESSAGE_SCALE = "Insufficient data to construct the scale matrix."

    def __init__(self, *data):
        """
        Matrix3x3 class constructor.
        If no data is provided, creates an identity matrix.
        Accepts:
        - a 3x3 matrix (numpy.ndarray),
        - a list of lists 2x2 or 3x3,
        - another Matrix3x3 object.
        """
        if len(data) == 0:
            # If no data is provided, creates an identity matrix
            self.data = np.eye(3, dtype=float)
        elif len(data) == 9:
            elements = np.array(data, dtype=float)
            self.data = elements.reshape((3, 3))
        elif len(data) == 4:
            elements = np.array(data, dtype=float)
            elements = elements.reshape((2, 2))
            self.data = np.eye(3, dtype=float)
            self.data[:2, :2] = elements
            pass
        elif len(data) == 1:
            data = data[0]
            if isinstance(data, Mat3x3):
                # If a Matrix3x3 object is passed
                self.data = np.copy(data.data)
            elif isinstance(data, (list, tuple, np.ndarray)):
                try:
                    data = np.array(data)
                    if data.shape == (3, 3):
                        # If a 3x3 matrix is passed
                        self.data = np.array(data, dtype=float)
                    elif data.shape == (2, 2):
                        # If a 2x2 matrix is passed, padded to 3x3
                        self.data = np.eye(3, dtype=float)
                        self.data[:2, :2] = data
                    else:
                        raise ValueError(Mat3x3.ERROR_MESSAGE_CONSTRUCTOR)
                except ValueError:
                    raise ValueError(Mat3x3.ERROR_MESSAGE_CONSTRUCTOR)

            else:
                raise ValueError(Mat3x3.ERROR_MESSAGE_CONSTRUCTOR)
        elif len(data) == 3 and all(isinstance(vec, Vec3) for vec in data):
            self.data = np.vstack([vec.data for vec in data])
        else:
            raise ValueError(Mat3x3.ERROR_MESSAGE_CONSTRUCTOR)

    def __getitem__(self, indices):
        """
        Get matrix element by indices (row, col).
        """
        row, col = indices
        return self.data[row, col]

    def __setitem__(self, indices, value):
        """
        Set matrix element value by indices (row, col).
        """
        row, col = indices
        self.data[row, col] = value

    def __str__(self):
        """
        Returns the string representation of the matrix.
        """
        return np.array2string(self.data, formatter={'float_kind': lambda x: f"{x:8.3f}"})

    def __add__(self, other):
        """
        Implements addition of two Matrix3x3 or numpy.ndarray 3x3 objects.
        """
        if not isinstance(other, (Mat3x3, np.ndarray)):
            raise TypeError(Mat3x3.ERROR_MESSAGE_ADD)
        if isinstance(other, Mat3x3):
            return Mat3x3(self.data + other.data)
        return Mat3x3(self.data + other)

    def __matmul__(self, other):
        """
        Implements matrix multiplication with another Matrix3x3, numpy.ndarray 3x3, or Vector3.
        """
        if not isinstance(other, (Mat3x3, np.ndarray, Vec3)):
            raise TypeError(Mat3x3.ERROR_MESSAGE_MULT)

        if isinstance(other, np.ndarray):
            if other.shape == (3,3):
                return self @ Mat3x3(other)
            elif other.shape == (3,):
                return self @ Vec3(other)
            else:
                raise TypeError(Mat3x3.ERROR_MESSAGE_MULT)

        if isinstance(other, Mat3x3):
            return Mat3x3(np.dot(self.data, other.data))
        if isinstance(other, Mat3x3):
            return Mat3x3(np.dot(self.data, other.data))
        elif isinstance(other, Vec3):
            return Vec3(np.dot(self.data, other.data))
        return Mat3x3(np.dot(self.data, other))

    def __mul__(self, other):
        """
        Implements matrix multiplication with another Matrix3x3, numpy.ndarray 3x3, or Vector3.
        """
        return self.__matmul__(other)

    def inverse(self):
        """
        Computes the inverse matrix.
        """
        det = np.linalg.det(self.data)
        if np.isclose(det, 0):
            raise ValueError(Mat3x3.ERROR_MESSAGE_INV_DOESNT_EXIST)
        return Mat3x3(np.linalg.inv(self.data))

    @staticmethod
    def identity():
        return Mat3x3(np.eye(3, dtype=float))

    @staticmethod
    def rotation(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)

        m = rotation_matrix_z(angle)
        return Mat3x3(m)

    @staticmethod
    def rotation_x(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)
        m = rotation_matrix_x(angle)
        return Mat3x3(m)

    @staticmethod
    def rotation_y(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)
        m = rotation_matrix_y(angle)
        return Mat3x3(m)

    @staticmethod
    def rotation_z(angle, is_radians=True):
        if not is_radians:
            angle = np.radians(angle)

        m = rotation_matrix_z(angle)
        return Mat3x3(m)

    @staticmethod
    def rotation_matrix_to_angle_axis(R):
        angle = np.arccos((R[0, 0] + R[1, 1] + R[2, 2] - 1) / 2)

        if np.isclose(angle, 0):
            axis = np.array([1, 0, 0])  # Axis is arbitrary since angle ≈ 0
        elif np.isclose(angle, np.pi):
            # Handle angle ≈ 180° carefully
            x = np.sqrt((R[0, 0] + 1) / 2)
            y = np.sqrt((R[1, 1] + 1) / 2)
            z = np.sqrt((R[2, 2] + 1) / 2)
            axis = np.array([x, y, z])
        else:
            axis = Vec3(
                R[2, 1] - R[1, 2],
                R[0, 2] - R[2, 0],
                R[1, 0] - R[0, 1]
            )
            axis = axis / (2 * np.sin(angle))

        return angle, axis

    def to_angle_axis(self):
        return Mat3x3.rotation_matrix_to_angle_axis(self)

    @staticmethod
    def translation(tx, ty=None):
        if ty is None and isinstance(tx, Vec3):
            m = translation_matrix2d(*tx.xy)
        elif ty is None and isinstance(tx, np.ndarray):
            m = translation_matrix2d(tx[0], tx[1])
        else:
            m = translation_matrix2d(tx, ty)
        return Mat3x3(m)

    @staticmethod
    def scale(*sx):
        if len(sx) == 1:
            sx = sx[0]
            if isinstance(sx, Vec3):
                m = scale_matrix(*sx.xyz)
            elif isinstance(sx, (np.ndarray, tuple, list)) and len(sx) <= 3:
                m = scale_matrix(*sx)
            elif isinstance(sx, (float, int)):
                m = scale_matrix(sx, sx, sx)
            else:
                raise ValueError(Mat3x3.ERROR_MESSAGE_SCALE)
        elif all(isinstance(el, (float, int)) for el in sx):
            m = scale_matrix(*sx)
        else:
            raise ValueError(Mat3x3.ERROR_MESSAGE_SCALE)
        return Mat3x3(m)


# Usage example
if __name__ == "__main__":
    # Initialization with various input types
    m1 = Mat3x3([[1, 2], [3, 4]])  # 2x2
    print("2x2 matrix padded to 3x3:")
    print(m1)

    m2 = Mat3x3([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # 3x3
    print("3x3 matrix:")
    print(m2)

    m22 = Mat3x3(([1, 2, 3], [4, 5, 6], [7, 8, 9]))  # 3x3 ########
    print("3x3 matrix:")
    print(m22)

    m3 = Mat3x3(m2)  # Copy об'єкта
    print("Copy of 3x3 matrix:")
    print(m3)

    # Access and modification of elements
    print("Element [1, 2]:", m2[1, 2])
    m2[1, 2] = 42
    print("Matrix after changing element [1, 2]:")
    print(m2)

    # Matrix multiplication
    m4 = m1 @ m2  # @ == *
    print("Matrix multiplication result:")
    print(m4)

    # Matrix addition
    m5 = m1 + m1
    print("Matrix addition result:")
    print(m5)

    # Element-wise matrix multiplication
    m6 = m2 * m2
    print("Matrix multiplication result:")
    print(m6)

    # Compute inverse matrix
    try:
        m1_inv = m1.inverse()
        print("Inverse of m1:")
        print(m1_inv)

        m8 = m1_inv * m1
        print("m7 * m1:")
        print(m8)
    except ValueError as e:
        print(f"Error: {e}")

    # v = Vector3(1, 2, 3)

    m33 = Mat3x3(1, 4, 6,
                 1, 3, 5,
                 34, 5, -7
                 )

    print(m33)

    m11 = Mat3x3(55, 66,
                 77, 88)
    print(m11)

    print("======== solving system of algebraic equations ===============")
    # print("A:")
    # print(m44)

    b = Vec3(1, 2, 4)
    print("b =", b)

    print("========= SCALE ===========")
    m22 = Mat3x3.scale(Vec3(2, 3, 4))
    print(m22)
    print()
    m22 = Mat3x3.scale((5, 6, 7))
    print(m22)
    print()

    m22 = Mat3x3.scale((5, 6))
    print(m22)
    print()

    m22 = Mat3x3.scale((5,))
    print(m22)
    print()

    print("========= SCALE 2 ===========")
    m22 = Mat3x3.scale(5)
    print(m22)
    print()

    m22 = Mat3x3.scale(5, 4)
    print(m22)
    print()
