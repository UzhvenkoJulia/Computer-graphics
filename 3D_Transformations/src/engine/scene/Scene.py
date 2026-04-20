from abc import ABC

import matplotlib
from matplotlib import pyplot as plt

from src.base.axes import draw_axes
from src.engine.scene.Frame import Frame, FrameCallback

matplotlib.use("TkAgg")


class Scene(ABC):

    def __init__(self,
                 image_size=(8, 8),
                 coordinate_rect=(-1, -1, -1, 1, 1, 1),
                 title="Picture",
                 base_axis_show=False,
                 grid_show=False,
                 axis_show=True,
                 axis_show_from_origin=True,
                 axis_color=("red", "green", "blue"),
                 axis_line_style="-.",
                 axis_line_width=1.0,
                 ):
        self.image_size = image_size
        self.coordinate_rect = coordinate_rect
        self.title = title
        self.base_axis_show = base_axis_show
        self.axis_show = axis_show
        self.axis_show_from_origin = axis_show_from_origin
        self.axis_color = axis_color
        self.axis_line_style = axis_line_style
        self.axis_line_width = axis_line_width
        self.grid_show = grid_show

        self.figure = plt.figure(figsize=self.image_size)
        self.plt_axis = self.figure.add_subplot(111, projection="3d")

        self.figures = {}

        self.frame_sequence: list[Frame] = []

    def add_figure(self, figure, name="default"):
        if name not in self.figures:
            self.figures[name] = figure
            figure.plt_axis = self.plt_axis
        else:
            raise KeyError(f"Figure name {name} already exists")

    def __setitem__(self, name, figure):
        self.add_figure(figure, name)

    def __getitem__(self, item):
        return self.figures[item]

    def __show_axes(self):
        if self.axis_show:
            draw_axes(
                self.plt_axis,
                self.coordinate_rect,
                self.axis_color,
                self.axis_line_style,
                linewidth=self.axis_line_width,
                axis_show_from_origin=self.axis_show_from_origin,
            )

        self.plt_axis.set_xlim([self.coordinate_rect[0], self.coordinate_rect[3]])
        self.plt_axis.set_ylim([self.coordinate_rect[1], self.coordinate_rect[4]])
        self.plt_axis.set_zlim([self.coordinate_rect[2], self.coordinate_rect[5]])

        # Equalise axis scale
        self.plt_axis.set_box_aspect([1, 1, 1])

    def __setup_view(self):
        self.plt_axis.view_init(elev=110,
                                azim=225,
                                roll=-45)

        # self.plt_axis.view_init(elev=110,
        #                         azim=245,
        #                         roll=-25)

    def __setup_base_parameters(self):
        # Disable default axes
        if not self.base_axis_show:
            self.plt_axis.axis('off')

        self.plt_axis.grid(self.grid_show)

    def __set_title(self):
        # Plot title
        self.plt_axis.set_title(self.title)

    def __draw(self, name=None):
        if name is None:
            self._draw_frames()
        elif name in self.figures:
            self[name].draw(self.plt_axis)
        else:
            raise KeyError("Figure {} doesn't exist to draw".format(name))

    def add_frames(self, *frames):
        for frame in frames:
            if isinstance(frame, Frame):
                self.frame_sequence.append(frame)
            elif callable(frame):
                self.frame_sequence.append(FrameCallback(frame))

    def _draw_frames(self):
        if len(self.frame_sequence) == 0:
            for name, figure in self.figures.items():
                figure.draw(self.plt_axis)
            return

        for frame in self.frame_sequence:
            frame.on_frame(self)

            for name, figure in self.figures.items():
                figure.draw(self.plt_axis)

    def _prepare(self):
        self.__setup_view()
        self.__set_title()
        self.__setup_base_parameters()
        self.__show_axes()

    @staticmethod
    def _show_plot():
        plt.show()

    def show(self):
        self._prepare()
        self.__draw()
        Scene._show_plot()
