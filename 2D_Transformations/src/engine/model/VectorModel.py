import numpy as np

from src.base.arrow import draw_segment
from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3, vertex


class VectorModel(Model):

    def __init__(self, *direction,
                 color="black",
                 line_style = "solid",
                 linewidth = 1.0,
                 label="",
                 label_color="black",
                 label_fontsize=DEFAULT_LABEL_FONT_SIZE,
                 label_offset=(0, 0)
                 ):
        super().__init__(*direction,
                         color=color,
                         line_style=line_style,
                         linewidth=linewidth
                         )
        self.label = label
        self.label_color = label_color
        self.label_fontsize = label_fontsize
        self.label_offset = label_offset

    def build_geometry(self, *vertices):
        direction = vertices
        _geometry = [vertex(0, 0)]

        if len(direction) == 1:
            item = direction[0]
            if isinstance(item, Vec3):
                _geometry.append(direction)
            elif isinstance(item, (np.ndarray, tuple, list)) and len(item) == 2:
                _geometry.append(vertex(*item))
        elif len(direction) == 2 and all(isinstance(item, (float, int)) for item in direction):
            _geometry.append(vertex(*direction))
        else:
            raise ValueError("Data corrupted")

        return _geometry

    def draw_model(self):
        transformed_geometry = self.transformed_geometry

        ps = [el.xy for el in transformed_geometry]

        draw_segment(*ps,
                     color=self.color,
                     label=self.label,
                     label_color=self.label_color,
                     label_fontsize=self.label_fontsize,
                     label_offset=self.label_offset
                     )

    def __setitem__(self, key, value):
        if key == "label":
            self.label = value
            return
        if key == "label_color":
            self.label_color = value
            return
        if key == "label_fontsize":
            self.label_fontsize = value
            return
        if key == "label_offset":
            self.label_offset = value
            return

        super().__setitem__(key, value)


if __name__ == '__main__':
    scene_figure_key = "vector"


    class SampleScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            v = VectorModel(1, 1)
            self[scene_figure_key] = v


    def frame1(scene: Scene):
        v : VectorModel = scene[scene_figure_key]

        v["color"] = "blue"
        v["label"] = "v"
        v["label_offset"] = -0.2, 0.1

    def frame2(scene: Scene):
        v: VectorModel = scene[scene_figure_key]

        v.translation = (1, 2)
        v.rotation = np.radians(20)


    sample_scene = SampleScene(
        coordinate_rect=(-1, -1, 5, 5),
        grid_show=False,
        axis_show=True
    )

    sample_scene.add_frames(frame1, frame2)

    sample_scene.show()
