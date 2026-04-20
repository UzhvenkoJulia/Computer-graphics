from src.engine.animation.Animation import Animation
from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import decompose_affine


class ScaleAnimation(Animation):

    def __init__(self, end, **kwargs):
        super().__init__(Mat4x4.scale(end), **kwargs)

    def current_transformation(self, frame):
        start_translation, start_rotation, start_scales, _, _ = decompose_affine(self.start)
        end_translation, end_rotation, end_scales, _, _ = decompose_affine(self.end_rotation)

        scales = start_scales + (end_scales - start_scales) * (frame / self.frames)

        T = Mat4x4.translation(start_translation)
        R = Mat4x4(start_rotation)
        S = Mat4x4.scale(*scales)

        transformation = T * R * S
        return transformation
