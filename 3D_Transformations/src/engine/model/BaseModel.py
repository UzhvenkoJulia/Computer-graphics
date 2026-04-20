from abc import abstractmethod, ABCMeta

import numpy as np

from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Vec4 import Vec4, vertex
from src.math.utils_matrix import decompose_translation_quaternion_scale, is_orthogonal


class BaseModel(metaclass=ABCMeta):

    def __init__(self, *vertices):
        self._pivot = vertex()
        self._geometry = self.build_geometry(*vertices)
        self._transformation = Mat4x4()

    def set_geometry(self, *vertices):
        self._geometry = self.build_geometry(*vertices)

    def __getitem__(self, item):
        return Vec4(self._geometry[item])

    def build_geometry(self, *vertices):
        if len(vertices) == 0:
            geometry = []
        elif all(isinstance(item, (float, int)) for item in vertices) and len(vertices) % 3 == 0:
            geometry = [vertex(vertices[i], vertices[i + 1], vertices[i + 2]) for i in range(0, len(vertices), 3)]
        elif all(isinstance(item, Vec4) for item in vertices):
            geometry = list(vertices)
        elif all(isinstance(item, np.ndarray) and item.shape == (3,) for item in vertices):
            geometry = [vertex(*item) for item in vertices]
        elif all(isinstance(item, (tuple, list)) and len(item) == 3 for item in vertices):
            geometry = [vertex(*item) for item in vertices]
        else:
            raise ValueError("Data corrupted")

        return geometry

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @property
    def rotation(self):
        translation, quaternion, scale = decompose_translation_quaternion_scale(self._transformation)
        return quaternion

    @rotation.setter
    def rotation(self, rotation):
        translation, quaternion, scale = decompose_translation_quaternion_scale(self._transformation)
        T = Mat4x4.translation(translation)
        S = Mat4x4.scale(scale)
        if isinstance(rotation, Quaternion):
            R =  rotation.toRotationMatrix()
        elif isinstance(rotation, Mat4x4):
            assert is_orthogonal(rotation), "Matrix of rotarion has to be orthogonal"
            R = rotation
        else:
            raise ValueError("Parameter 'rotation' isn't actually rotation")

        self.transformation = T * R * S

    @property
    def scale(self):
        translation, quaternion, scale = decompose_translation_quaternion_scale(self._transformation)
        return scale

    @scale.setter
    def scale(self, scale):
        translation, quaternion, curr_scale = decompose_translation_quaternion_scale(self._transformation)
        T = Mat4x4.translation(translation)
        S = Mat4x4.scale(scale)
        R = quaternion.toRotationMatrix()
        self.transformation = T * R * S

    @property
    def translation(self):
        translation, quaternion, scale = decompose_translation_quaternion_scale(self._transformation)
        return translation

    @translation.setter
    def translation(self, translation):
        curr_translation, quaternion, scale = decompose_translation_quaternion_scale(self._transformation)
        T = Mat4x4.translation(translation)
        S = Mat4x4.scale(scale)
        R = quaternion.toRotationMatrix()
        self.transformation = T * R * S


    @property
    def transformed_geometry(self):
        p = Mat4x4.translation(self._pivot)
        p_inv = p.inverse()
        transformation = p * self.transformation * p_inv
        transformed_data = [transformation * point for point in self._geometry]

        return transformed_data

    def apply_transformation_to_geometry(self):
        self._geometry = self.transformed_geometry
        self.transformation = Mat4x4()

    def pivot(self, tx, ty=None, tz=None):
        if ty is None and isinstance(tx, Vec4):
            self._pivot = tx
        else:
            self._pivot = Vec4(tx, ty, tz, 1)

    def draw(self, plt_axis):
        self.draw_model(plt_axis)

    @abstractmethod
    def draw_model(self, plt_axis):
        pass
