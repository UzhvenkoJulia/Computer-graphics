from src.engine.animation.Animation import Animation
from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import decompose_translation_quaternion_scale
from src.math.utils_quat import slerp


class QuaternionAnimation(Animation):

    def __init__(self, end_quaternion, **kwargs):  # end - Quaternion
        super().__init__(end_quaternion, **kwargs)
        self.start_translation, self.start_rotation, self.start_scale = decompose_translation_quaternion_scale(self.start)
        self.end_rotation = end_quaternion

    def current_transformation(self, frame):
        t = frame / self.frames

        q0 = self.start_rotation
        q1 = self.end_rotation

        interpolated = slerp(q0, q1, t)

        T = Mat4x4.translation(self.start_translation)
        R = interpolated.toRotationMatrix()
        S = Mat4x4.scale(self.start_scale)

        transformation = T * R * S
        return transformation
