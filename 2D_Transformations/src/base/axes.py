from matplotlib import pyplot as plt


def draw_axis(start, end,
              color="black", linewidth=1.0, linestyle=":",
              head_width_coef=0.1, head_length_coef = 0.1,
              ):
    plt.plot([start[0], end[0]], [start[1], end[1]],
             color=color,
             linestyle=linestyle,
             linewidth=linewidth
             )

    u, v = end[0] - start[0], end[1] - start[1]

    plt.arrow(
        end[0], end[1], u * 0.015, v * 0.015,
        head_width=linewidth * head_width_coef,
        head_length=linewidth * head_length_coef,
        fc=color, ec=color,
        linewidth=linewidth
    )


def draw_axes(coordinate_rect, axis_color, axis_line_style, linewidth=1.0):
    shift_offset = 0.1

    y_len = coordinate_rect[3] - coordinate_rect[1]
    shift = y_len * shift_offset / 2

    start_x = (0.0, coordinate_rect[1] + shift)
    end_x = (0.0, coordinate_rect[3] - shift)

    axis_x_color = "red"
    axis_y_color = "green"
    if isinstance(axis_color, str):
        axis_x_color = axis_color
        axis_y_color = axis_color
    elif isinstance(axis_color, (tuple, list)):
        if len(axis_color) == 1:
            axis_x_color = axis_color
            axis_y_color = axis_color
        elif len(axis_color) >= 2:
            axis_x_color = axis_color[0]
            axis_y_color = axis_color[1]

    draw_axis(start_x, end_x, color=axis_y_color, linestyle=axis_line_style, linewidth=linewidth)

    x_len = coordinate_rect[2] - coordinate_rect[0]
    x_shift = x_len * shift_offset / 2

    start_x = (coordinate_rect[0] + x_shift, 0.0)
    end_x = (coordinate_rect[2] - x_shift, 0.0)
    draw_axis(start_x, end_x, color=axis_x_color, linestyle=axis_line_style, linewidth=linewidth)
