from src.base.axes import draw_axis
from src.engine.model.BaseModel import BaseModel


class CoordinateFrame(BaseModel):

    def __init__(self):
        super().__init__(
            0, 0, 0,
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
        )

        self.color = ("red", "green", "blue")
        self.line_style = "-"
        self.line_width = 1.0

    def set_parameters(self,
                       color=None,
                       line_width=None,
                       line_style=None
                       ):

        if color is not None:
            if isinstance(color, str):
                self.color = (color, color, color)
            elif isinstance(color, (tuple, list)) and len(color) == 3:
                self.color = tuple(color)  # coordinate axis color

        if line_width is not None:
            self.line_width = line_width  # coordinate axis width
        if line_style is not None:
            self.line_style = line_style  # coordinate axis line style

    def draw_model(self, plt_axis):
        transformed_geometry = self.transformed_geometry
        ps = [el.xyz for el in transformed_geometry]

        origin = ps[0]
        ox = ps[1]
        oy = ps[2]
        oz = ps[3]

        draw_axis(
            plt_axis,
            origin, ox,
            color=self.color[0],
            linewidth=self.line_width,
            linestyle=self.line_style
        )

        draw_axis(
            plt_axis,
            origin, oy,
            color=self.color[1],
            linewidth=self.line_width,
            linestyle=self.line_style
        )

        draw_axis(
            plt_axis,
            origin, oz,
            color=self.color[2],
            linewidth=self.line_width,
            linestyle=self.line_style
        )
