import numpy as np

from src.base.text import print_label
from src.engine.model.VectorModel import VectorModel
from src.engine.scene.Scene import Scene
from src.base.axes import draw_axis
from src.math.Vec3 import vertex


class Axis(VectorModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_length_coef = 0.1
        self.head_width_coef = 0.05

    def build_geometry(self, *vertices):
        if len(vertices) == 2 and all(isinstance(item, (float, int, np.int64)) for item in vertices):
            return [vertex(0, 0), vertex(*vertices)]

        if len(vertices) == 4 and all(isinstance(item, (float, int, np.int64)) for item in vertices):
            return [vertex(vertices[0], vertices[1]), vertex(vertices[2], vertices[3])]

        if len(vertices) == 2 and all(isinstance(item, (np.ndarray, tuple, list)) for item in vertices):
            return [vertex(*vertices[0]), vertex(*vertices[1])]

        if len(vertices) == 1 and all(isinstance(item, (np.ndarray, tuple, list)) for item in vertices):
            return [vertex(), vertex(*vertices[0])]



        raise ValueError("Data corrupted")


    def __setitem__(self, key, value):
        if key == "head_width_coef":
            self.head_width_coef = value
            return
        if key == "head_length_coef":
            self.head_length_coef = value
            return

        super().__setitem__(key, value)

    def draw_model(self):
        transformed_geometry = self.transformed_geometry
        ps = [el.xy for el in transformed_geometry]

        draw_axis(
            ps[0], # origin
            ps[1], # direction
            color=self.color,
            linewidth=self.linewidth,
            linestyle=self.line_style,
            head_length_coef=self.head_length_coef,
            head_width_coef=self.head_width_coef,
        )

        print_label(start=np.array(ps[1]) ,
                    label=self.label,
                    label_color=self.label_color,
                    label_fontsize=self.label_fontsize,
                    label_offset=self.label_offset)



if __name__ == '__main__':
    OX_ID = "OX_ID"
    OY_ID = "OY_ID"
    OZ_ID = "OZ_ID"




    simple_scene = Scene(
        coordinate_rect=(-3.5, -3.5, 3.5, 3.5),  # розмірність системи координатps
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=False,  # чи показувати осі координат
        # axis_color="grey",  # колір осей координат
        # axis_line_style="-."  # стиль ліній осей координат
    )

    v_dir = 1.6, 0.9
    v_proj_oxy_ccords =  v_dir[0], -0.6

    Ox = Axis(2.9, 0, color="red", linewidth=1.5, label="$x$", label_offset=(0.1, 0.1))
    Oy = Axis(0, 2.4, color="green", linewidth=1.5, label="$y$", label_offset=(0.1, 0.2))
    Oz = Axis(-1.4, -1.2, color="blue", linewidth=1.5, label="$z$", label_offset=(-0.35, -0.3))
    v = Axis(v_dir, color="brown", linewidth=1.5, label="$v$", label_offset=(0.1, 0.2))
    v_proj_oxy = Axis(v_dir, v_proj_oxy_ccords, color="brown", linewidth=1., line_style="--", label="$v$", label_offset=(0.1, 0.2))

    simple_scene[OX_ID] = Ox
    simple_scene[OY_ID] = Oy
    simple_scene[OZ_ID] = Oz
    simple_scene["v"] = v
    simple_scene["v_proj"] = v_proj_oxy


    simple_scene.show()