import numpy as np


def draw_axis(plt_axis, start, end,
              color="black", linewidth=1.0, linestyle=":", ):
    plt_axis.plot((start[0], end[0]), (start[1], end[1]), (start[2], end[2]),
                  color=color,
                  linewidth=linewidth,
                  linestyle=linestyle, )

    u = np.array((end[0] - start[0], end[1] - start[1], end[2] - start[2])) * 0.15
    plt_axis.quiver(*end[:3], *u,
                    color=color,
                    linewidth=linewidth,
                    arrow_length_ratio=1
                    # linestyle=linestyle,
                    )


def draw_axes(plt_axis, coordinate_rect,
              axis_color,
              axis_line_style,
              linewidth=1.0,
              axis_show_from_origin=True):
    ######### color ##############
    axis_x_color = "red"
    axis_y_color = "green"
    axis_z_color = "blue"
    if isinstance(axis_color, str):
        axis_x_color = axis_color
        axis_y_color = axis_color
        axis_z_color = axis_color
    elif isinstance(axis_color, (tuple, list)):
        if len(axis_color) == 1:
            axis_x_color = axis_color[0]
            axis_y_color = axis_color[0]
            axis_z_color = axis_color[0]
        elif len(axis_color) >= 3:
            axis_x_color = axis_color[0]
            axis_y_color = axis_color[1]
            axis_z_color = axis_color[2]

    ######### geometry ##############

    shift_offset = 0.1

    left_bottom_far = np.array(coordinate_rect[:3])
    right_top_near = np.array(coordinate_rect[3:])

    delta = right_top_near - left_bottom_far

    x_len = abs(delta[0])
    y_len = abs(delta[1])
    z_len = abs(delta[2])

    shift_x = x_len * shift_offset / 2
    shift_y = y_len * shift_offset / 2
    shift_z = z_len * shift_offset / 2

    origin = (0.0, 0.0, 0.0)

    start_x = origin if axis_show_from_origin else (coordinate_rect[0] + shift_x, 0.0, 0.0)
    end_x = (coordinate_rect[3] - shift_x, 0.0, 0.0)

    start_y = origin if axis_show_from_origin else (0.0, coordinate_rect[1] + shift_y, 0.0)
    end_y = (0.0, coordinate_rect[4] - shift_y, 0.0)

    start_z = origin if axis_show_from_origin else (0.0, 0.0, coordinate_rect[2] + shift_z)
    end_z = (0.0, 0.0, coordinate_rect[5] - shift_z)

    draw_axis(plt_axis, start_x, end_x, color=axis_x_color, linestyle=axis_line_style, linewidth=linewidth)
    draw_axis(plt_axis, start_y, end_y, color=axis_y_color, linestyle=axis_line_style, linewidth=linewidth)
    draw_axis(plt_axis, start_z, end_z, color=axis_z_color, linestyle=axis_line_style, linewidth=linewidth)
