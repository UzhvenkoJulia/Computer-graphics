from src.engine.animation.Animation import Animation
from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import decompose_affine


class TrsTransformationAnimation(Animation):


    def current_transformation(self, frame):
        start_translation, start_rotation, start_scale, start_axis, start_angle = decompose_affine(self.start)
        end_translation, end_rotation, end_scale, end_axis, end_angle = decompose_affine(self.end_rotation)

        t = frame / self.frames

        translation = start_translation + (end_translation - start_translation) * t
        angle = start_angle + (end_angle - start_angle) * t
        scales = start_scale + (end_scale - start_scale) * t

        T = Mat4x4.translation(translation)
        R = Mat4x4.rotation(angle, end_axis)
        S = Mat4x4.scale(scales)

        transformation = T * R * S
        return transformation
