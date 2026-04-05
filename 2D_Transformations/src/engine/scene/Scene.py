from abc import ABC

from matplotlib import pyplot as plt

from src.base.axes import draw_axes
from src.engine.scene.Frame import Frame, FrameCallback


class Scene(ABC):

    def __init__(self,
                 image_size=(8, 8),
                 coordinate_rect=(-1, -1, 1, 1),
                 title="Picture",
                 base_axis_show=True,
                 axis_show=False,
                 axis_color=("red", "green"),
                 axis_line_style="-.",
                 axis_line_width=1.0,
                 grid_show=True,
                 grid_line_linestyle="solid",
                 greed_alpha=1.0,
                 keep_aspect_ratio=True,
                 out_file = None,
                 ):
        self.image_size = image_size
        self.coordinate_rect = coordinate_rect
        self.title = title
        self.base_axis_show = base_axis_show
        self.axis_show = axis_show
        self.axis_color = axis_color
        self.axis_line_style = axis_line_style
        self.axis_line_width = axis_line_width
        self.grid_show = grid_show
        self.grid_line_linestyle = grid_line_linestyle
        self.greed_alpha = greed_alpha
        self.keep_aspect_ratio = keep_aspect_ratio
        self.out_file = out_file
        self.figure = plt.figure(figsize=self.image_size)
        self.figures = {}

        self.frame_sequence: list[Frame] = []

    def add_figure(self, figure, name="default"):
        if name not in self.figures:
            self.figures[name] = figure
        else:
            raise KeyError("Figure name {} already exists".format(name))

    def get_figure(self, name):
        return self.figures[name]

    def __setitem__(self, name, figure):
        self.add_figure(figure, name)

    def __getitem__(self, item):
        return self.figures[item]

    def __show_axes(self):
        if self.axis_show:
            draw_axes(self.coordinate_rect, self.axis_color, self.axis_line_style, self.axis_line_width)

        plt.xlim(self.coordinate_rect[0], self.coordinate_rect[2])
        plt.ylim(self.coordinate_rect[1], self.coordinate_rect[3])

    def __setup_base_parameters(self):
        # Відключення стандартних осей
        if not self.base_axis_show:
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)

        if self.keep_aspect_ratio:
            plt.gca().set_aspect('equal', adjustable='box')

        if self.grid_show:
            plt.grid(self.grid_show, linestyle=self.grid_line_linestyle, alpha=self.greed_alpha, )
        else:
            plt.grid(False)

    def __set_title(self):
        plt.title(self.title)

    def draw(self, name=None):
        if name is None:
            self._draw_frames()
        elif name in self.figures:
            self[name].draw()
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
                figure.draw()
            return

        for frame in self.frame_sequence:
            frame.on_frame(self)

            for name, figure in self.figures.items():
                figure.draw()

    def _prepare(self):
        self.__set_title()
        self.__setup_base_parameters()
        self.__show_axes()

    @staticmethod
    def _show_plot():
        plt.show()

    def show(self, output_file=None):
        self._prepare()
        self.draw()

        if output_file is None:
            Scene._show_plot()
        else:
            plt.savefig(output_file)
