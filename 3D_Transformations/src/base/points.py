from src.base.text import DEFAULT_LABEL_FONT_SIZE, print_label


def draw_point(plt_axis, start, size=50,
               color="black",
               label="",
               label_color="black", label_fontsize=DEFAULT_LABEL_FONT_SIZE, label_offset=(0, 0)
               ):
    plt_axis.scatter(*start, color=color, s=size, label=label, )  # s - point size

    print_label(
        plt_axis,
        start=start,
        label=label,
        label_color=label_color,
        label_fontsize=label_fontsize,
        label_offset=label_offset
    )
