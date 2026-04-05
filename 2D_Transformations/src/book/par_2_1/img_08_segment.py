import numpy as np

from src.engine.model.LineModel import LineModel
from src.engine.model.Point import SimplePoint
from src.engine.scene.Scene import Scene

FIGURE_LINE = "LINE_FIGURE"
FIGURE_VECTOR = "FIGURE_VECTOR"
FIGURE_POINT = "FIGURE_POINT"
if __name__ == '__main__':

    class LineScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            P = np.array([1, 1])
            Q = np.array([2.5, 2.5])

            line = LineModel(P, Q)
            line.linewidth = 3
            line["color"] = "blue"
            line["line_style"] = "solid"
            self[FIGURE_LINE] = line


            p = SimplePoint(P, Q)
            p["color"] = "red"
            p["labels"] = (("$P$", (-0.2, -0.5)),
                           ("$Q$", (-0.1, 0.2)))
            p["label_color"] = "red"
            p["label_fontsize"] = 28
            self[FIGURE_POINT] = p

            # dir = Q-P
            # v = VectorModel(dir)
            # # v.scale = (0.3, 0.3)
            # v["color"] = "blue"
            # v["line_width"] = 0.5
            # v["label"] = "$v$"
            # v["label_offset"] = -0.3, 0.1
            # v["label_fontsize"] = 28
            # v.translation = (1, 1)
            # self[FIGURE_VECTOR] = v





    def frame1(scene: Scene):
        line : LineModel = scene[FIGURE_LINE]

        # line["color"] = "blue"


    def frame2(scene: Scene):
        line: LineModel = scene[FIGURE_LINE]

        line["line_style"] = ":"

        line.translation = (1, 2)
        line.rotation = np.radians(20)


    sample_scene = LineScene(
        coordinate_rect=(-1, -1, 5, 5),
        grid_show=False,
        axis_show=True
    )

    sample_scene.add_frames(
        frame1,
        # frame2
    )

    sample_scene.show()

