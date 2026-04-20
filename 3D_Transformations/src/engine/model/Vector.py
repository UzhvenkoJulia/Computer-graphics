from src.base.axes import draw_axis
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene


class Vector(Model):

    def __init__(self,
                 *vertices,
                 color="grey",
                 linestyle="-",
                 linewidth=1.0,
                 ):
        super().__init__(*vertices, color=color)

        self.linestyle = linestyle
        self.linewidth = linewidth

    def draw_model(self, plt_axis):
        transformed_geometry = self.transformed_geometry
        ps = [el.xyz for el in transformed_geometry]

        draw_axis(
            plt_axis,
            ps[0], ps[1],
            color=self.color,
            linewidth=self.linewidth,
            linestyle=self.linestyle
        )


if __name__ == '__main__':
    VECT_KEY = "rect"

    class VectorScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self[VECT_KEY] = Vector(
                            0, 0, 0,
                            0.557, 0.500, 0.663,
                            color="brown"
                            )

    simple_scene = VectorScene()
    simple_scene.show()
