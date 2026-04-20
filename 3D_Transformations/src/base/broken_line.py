def draw_broken_line(plt_axis,
                     line_points,
                     color="black",
                     linewidth=1.0, linestyle="solid",
                     vertices_show=False, vertex_color="black", vertex_size=50,
                     # labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,
                     ):
    x = []
    y = []
    z = []
    for a, b, c in line_points:
        x.append(a)
        y.append(b)
        z.append(c)


    plt_axis.plot3D(x, y, z,
                    color=color,
                    linewidth=linewidth,
                    linestyle=linestyle)
    pass
    # draw_points(x, y,
    #             vertices_show=vertices_show,
    #             vertex_color=vertex_color,
    #             vertex_size=vertex_size,
    #             labels=labels,
    #             labels_color=labels_color,
    #             labels_font_size=labels_font_size,
    #             )



