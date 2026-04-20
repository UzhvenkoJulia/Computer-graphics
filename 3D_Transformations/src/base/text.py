import numpy as np

from src.engine.scene.Scene import Scene

DEFAULT_LABEL_FONT_SIZE = 20


def print_label(
        plt_axis,
        start,
        label="", label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0, 0)):
    if label is not None and label != "":
        label_pos = np.array(start) + label_offset
        plt_axis.text(float(label_pos[0]),
                      float(label_pos[1]),
                      float(label_pos[2]),
                      label, fontsize=label_fontsize, color=label_color,
                      ha='left')


if __name__ == '__main__':
    def frame1(scene):
        print_label(
            scene.plt_axis,
            start=(0.5, 0.5, 0.5),
            label=r"Hello $R_2^4$", label_color="red", label_fontsize=22,
            label_offset=(-0.2, 0.1, 0.0))

        print_label(
            scene.plt_axis,
            start=(0.5, 0.2, 0.5),
            label=r"Water $H_20$", label_color="green", label_fontsize=13,
            label_offset=(-0.2, 0.1, 0.0))


    scene = Scene(
        coordinate_rect=(0, 0, 0, 1, 1, 1),
        grid_show=True,
    )
    scene.add_frames(frame1)
    scene.show()
