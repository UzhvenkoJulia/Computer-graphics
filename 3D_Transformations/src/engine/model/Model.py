from abc import ABC

from src.base.points import draw_point
from src.engine.model.BaseModel import BaseModel
from src.engine.model.CoordinateFrame import CoordinateFrame
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import vertex


class Model(BaseModel, ABC):

    def __init__(self,
                 *vertices,
                 color="grey"
                 ):
        super().__init__(*vertices)

        self._pivot = vertex()
        self._is_draw_pivot = False

        self._coord_frame = CoordinateFrame()

        self._is_draw_local_frame = False

        self.color = color

    def show_pivot(self, enabled=True):
        self._is_draw_pivot = enabled

    def pivot(self, tx, ty=None, tz=None):
        super().pivot(tx, ty, tz)
        self._coord_frame.pivot(tx, ty, tz)

    def show_local_frame(self, enabled=True):
        self._is_draw_local_frame = enabled

    def set_local_frame_parameters(self,
                                   color=None,
                                   line_width=None,
                                   line_style=None
                                   ):
        self._coord_frame.set_parameters(
            color=color,
            line_width=line_width,
            line_style=line_style
        )

    def _draw_local_frame(self, plt_axis):
        if self._is_draw_local_frame:
            self._coord_frame.transformation = self._transformation
            self._coord_frame.pivot(self._pivot)
            self._coord_frame.draw_model(plt_axis)

    def _draw_pivot(self, plt_axis):
        if self._is_draw_pivot:
            p = Mat4x4.translation(self._pivot)
            pivot = p * self.transformation * p.inverse() * self._pivot
            draw_point(plt_axis, pivot.xyz, color="red")

    def apply_transformation_to_geometry(self):
        super().apply_transformation_to_geometry()

        self._coord_frame.apply_transformation_to_geometry()

    def draw(self, plt_axis):
        self._draw_local_frame(plt_axis)

        super().draw(plt_axis)

        self._draw_pivot(plt_axis)
