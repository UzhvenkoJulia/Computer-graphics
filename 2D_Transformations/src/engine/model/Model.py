from abc import ABC

from src.base.points import draw_point
from src.engine.model.BaseModel import BaseModel
from src.engine.model.CoordinateFrame import CoordinateFrame
from src.math.Mat3x3 import Mat3x3
from src.math.Vec3 import vertex


class Model(BaseModel, ABC):

    def __init__(self,
                 *vertices,
                 color = "grey",
                 line_style="solid",
                 linewidth=1.0,
                 ):
        super().__init__(*vertices)

        self._pivot = vertex()
        self._is_draw_pivot = False

        self._coord_frame = CoordinateFrame()
        self._is_draw_local_frame = False

        self.color = color
        self.line_style = line_style
        self.linewidth = linewidth

    def __setitem__(self, key, value):
        if key == "color":
            self.color = value
            return
        if key == "line_style":
            self.line_style = value
            return
        if key == "linewidth":
            self.linewidth = value
            return

        super().__setitem__(key, value)

    def show_pivot(self, enabled=True):
        self._is_draw_pivot = enabled

    def pivot(self, tx, ty=None, tz=None):
        super().pivot(tx, ty)
        self._coord_frame.pivot(tx, ty)

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

    def _draw_local_frame(self):
        if self._is_draw_local_frame:
            self._coord_frame.transformation = self.transformation
            self._coord_frame.draw_model()

    def _draw_pivot(self):
        if self._is_draw_pivot:
            p = Mat3x3.translation(self._pivot)
            pivot = p * self.transformation * p.inverse() * self._pivot
            draw_point(pivot.xy, color="red")

    def apply_transformation_to_geometry(self):
        super().apply_transformation_to_geometry()

        self._coord_frame.apply_transformation_to_geometry()

    def draw(self):
        self._draw_local_frame()

        super().draw()

        self._draw_pivot()
