import matplotlib.pyplot as plt
import numpy as np

from src.base.arrow import draw_vector
from src.base.broken_line import draw_broken_line
from src.base.text import DEFAULT_LABEL_FONT_SIZE
from src.engine.scene.Scene import Scene


def draw_arc(origin, v1, v2,
             radius=1.0,  # Радіус дуги
             color="black",
             linestyle="solid", linewidth=1.0,
             reverse=False,
             num_points = 10, # Кількість точок дуги
             ):
    # Кути між векторами
    theta1 = np.arctan2(v1[1], v1[0])  # Кут першого вектора
    theta2 = np.arctan2(v2[1], v2[0])  # Кут другого вектора

    # Якщо потрібно намалювати дугу з іншого боку
    if reverse:
        if theta1 < theta2:
            theta2 -= 2 * np.pi  # Йдемо у від'ємному напрямку
        else:
            theta2 += 2 * np.pi  # Йдемо у додатному напрямку

    # Генерація точок дуги
    angles = np.linspace(theta1, theta2, num_points)  # Усі кути між двома векторами

    x_arc = origin[0] + radius * np.cos(angles)  # X-координати дуги
    y_arc = origin[1] + radius * np.sin(angles)  # Y-координати дуги

    # Малювання дуги
    plt.plot(x_arc, y_arc, color=color, linestyle=linestyle, linewidth=linewidth, label="Дуга")


def draw_fake_rectangular_arc(
        origin, v1, v2,
        scale=1.0,  # Радіус дуги
        color="black",
        linestyle="solid", linewidth=1.0,
        vertex_color="black", vertex_size=50,
        labels=(), labels_color="black", labels_font_size=DEFAULT_LABEL_FONT_SIZE,

):
    # Розрахунок координат для прямого кута
    v1_unit = v1 / np.linalg.norm(v1)  # Одиничний вектор v1
    v2_unit = v2 / np.linalg.norm(v2)  # Одиничний вектор v2

    corner = origin + scale * v1_unit  # Перша точка кута (вздовж v1)
    corner2 = corner + scale * v2_unit  # Друга точка кута (вздовж v2)
    corner3 = origin + scale * v2_unit

    draw_broken_line([corner, corner2, corner3],
                     color=color,
                     line_style=linestyle, linewidth=linewidth,
                     vertex_color=vertex_color, vertex_size=vertex_size,
                     labels=labels,  # Підписи вершин
                     labels_color=labels_color, labels_font_size=labels_font_size
                     )


if __name__ == '__main__':

    def frame1(self):
        # Центр (початок координат)
        origin = np.array([0.5, 0.5])

        # Вектори
        v1 = np.array([1, -1.3])  # Перший вектор
        v2 = np.array([0.5, 0.866])  # Другий вектор (утворює 60 градусів з першим)

        draw_arc(origin, v1, v2,
                 radius=0.25,
                 color="red",
                 linestyle="--", linewidth=1.0,
                 )

        # # Малювання векторів
        draw_vector(origin, v1, color='blue', label=r"$v_1$")
        draw_vector(origin, v2, color='green', label=r"$v_2$")

        # perpendicular
        v1 = np.array([-1, -1.5])  # Перший вектор
        v2 = np.array([-1, 1])  # Другий вектор
        origin = origin + (-1.0, -1.0)
        draw_vector(origin, v1, color='brown', label=r"$v_1$")
        draw_vector(origin, v2, color='red', label=r"$v_2$")

        labels = [('A', (0.1, -0.3)),
                  ('B', (-0.3, 0.0)),
                  ('C', (-0.1, 0.2)),
                  ]  # Підписи вершин
        draw_fake_rectangular_arc(origin, v1, v2,
                                  scale=0.25,
                                  color="green",
                                  linestyle="--", linewidth=1.0,
                                  labels=labels,
                                  labels_color="crimson",
                                  vertex_color="yellow",
                                  )

    scene = Scene(
        coordinate_rect=(-2, -2, 2, 2),
        # grid_show=False,
        base_axis_show=False,
        axis_show=True,
        axis_color="red",
        axis_line_style="-."
    )
    scene.add_frames(frame1)
    scene.show()
