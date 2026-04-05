import numpy as np

from src.base.broken_line import draw_broken_line
from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene


class Polygon(Model):

    def __init__(self, *vertices,
                 color="black",
                 linewidth=1.0,
                 line_style="solid",
                 vertices_show=False, vertex_color="black", vertex_size=50,
                 labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,
                 ):
        super().__init__(*vertices, color=color, linewidth=linewidth, line_style=line_style)

        self.vertices_show = vertices_show
        self.vertex_color = vertex_color
        self.vertex_size = vertex_size
        self.linewidth = linewidth
        self.line_style = line_style
        self.labels = labels
        self.labels_color = labels_color
        self.labels_font_size = labels_font_size

    def draw_model(self):
        transformed_geometry = self.transformed_geometry

        ps = [el.xy for el in transformed_geometry]
        ps.append(transformed_geometry[0].xy)  # closed line

        draw_broken_line(ps, color=self.color,
                         vertices_show=self.vertices_show,
                         vertex_color=self.vertex_color,
                         vertex_size=self.vertex_size,
                         linewidth=self.linewidth,
                         line_style=self.line_style,
                         labels=self.labels,
                         labels_color=self.labels_color,
                         labels_font_size=self.labels_font_size,)


    def __setitem__(self, key, value):
        if key == "vertices_show":
            self.vertices_show = value
            return
        if key == "vertex_color":
            self.vertex_color = value
            return
        if key == "vertex_size":
            self.vertex_size = value
            return
        if key == "labels":
            self.labels = value
            return
        if key == "labels_color":
            self.labels_color = value
            return
        if key == "labels_fontsize":
            self.labels_fontsize = value
            return

        super().__setitem__(key, value)

if __name__ == '__main__':
    scene_figure_key = "polygon"

    class PolygonScene(Scene):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            m = Polygon(
                0, 0,
                1, 0,
                1, 1,
                0, 1
            )

            self[scene_figure_key] = m

    polygon_scene = PolygonScene(
        coordinate_rect=(-1, -1, 3, 3),
        # grid_show=False,
        base_axis_show=False,
        axis_show=True,
        axis_color="red",
        axis_line_style="-."
    )


    def frame1(scene: Scene):
        m: Polygon = scene[scene_figure_key]

        m.pivot(0.5, 0.5)
        m.show_pivot()

        m["color"] = "green"
        m["line_style"] = "--"


    def frame2(scene: Scene):
        m: Polygon = scene[scene_figure_key]
        m["color"] = "blue"
        m["line_style"] = "solid"

        m.rotation = np.radians(45)


    polygon_scene.add_frames(frame1,
                             frame2
                             )

    polygon_scene.show()
