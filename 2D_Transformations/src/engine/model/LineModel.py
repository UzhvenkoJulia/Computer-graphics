import numpy as np

from src.base.lines import draw_line
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3, vertex


class LineModel(Model):

    def __init__(self, *direction,
                 color="black",
                 line_style = "solid",
                 linewidth = "1.0",
                 ):
        super().__init__(*direction,
                         color=color,
                         line_style=line_style,
                         linewidth=linewidth
                         )

    def build_geometry(self, *vertices):
        _geometry = []

        if len(vertices) == 4 and all(isinstance(item, (float, int)) for item in vertices):
            _geometry.append(vertex(vertices[0], vertices[1]))
            _geometry.append(vertex(vertices[2], vertices[3]))
        elif len(vertices) == 2:
            if all(isinstance(item, (np.ndarray, tuple, list)) and len(item) == 2 for item in vertices):
                _geometry.append(vertex(*vertices[0]))
                _geometry.append(vertex(*vertices[1]))
            elif all(isinstance(item, Vec3) for item in vertices):
                _geometry.append(vertices[0])
                _geometry.append(vertices[1])
            else:
                raise ValueError("Data corrupted")
        else:
            raise ValueError("Data corrupted")

        return _geometry

    def draw_model(self):
        transformed_geometry = self.transformed_geometry

        ps = [el.xy for el in transformed_geometry]

        draw_line(*ps,
                  color=self.color,
                  linestyle=self.line_style,
                  linewidth=self.linewidth)


if __name__ == '__main__':
    scene_figure_key = "vector"


    class SampleScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # v = LineModel(1, 1, 2, 2,)
            v = LineModel(vertex(1, 1), vertex(2, 2),)
            self[scene_figure_key] = v


    def frame1(scene: Scene):
        v : LineModel = scene[scene_figure_key]

        v["color"] = "blue"


    def frame2(scene: Scene):
        v: LineModel = scene[scene_figure_key]

        v["line_style"] = ":"

        v.translation = (1, 2)
        v.rotation = np.radians(20)


    sample_scene = SampleScene(
        coordinate_rect=(-1, -1, 5, 5),
        grid_show=False,
        axis_show=True
    )

    sample_scene.add_frames(
        frame1,
        frame2
    )

    sample_scene.show()
