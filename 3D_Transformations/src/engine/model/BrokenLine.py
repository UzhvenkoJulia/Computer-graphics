from src.base.broken_line import draw_broken_line
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene


class BrokenLine(Model):

    def __init__(self,
                 *vertices,
                 color="black",
                 linewidth=1.0,
                 linestyle="solid",
                 ):
        super().__init__(*vertices, color=color)

        self.linestyle = linestyle
        self.linewidth = linewidth

    def draw_model(self, plt_axis):
        transformed_geometry = self.transformed_geometry
        ps = [el.xyz for el in transformed_geometry]

        draw_broken_line(
            plt_axis,
            ps,
            color=self.color,
            linewidth=self.linewidth,
            linestyle=self.linestyle
        )


if __name__ == '__main__':
    MODEL_KEY = "model"


    class LineScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self[MODEL_KEY] = BrokenLine(
                0, 0, 0,
                0.557, 0.500, 0.663,
                1, 1, 1,
                -1, 1, 1,
                0, 0, 0,
                color="brown"
            )



    ############## Frame 1 ##################
    def frame1(scene: Scene):
        vector: BrokenLine = scene[MODEL_KEY]
        print("initial geom")
        print(vector.transformed_geometry[1].xyz)


    simple_scene = LineScene()

    simple_scene.add_frames(
        frame1,
    )  # add frames to the scene

    simple_scene.show()
