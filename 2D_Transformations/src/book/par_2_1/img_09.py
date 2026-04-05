import numpy as np

from src.base.arrow import draw_vector
from src.base.lines import draw_line
from src.base.text import print_label
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
        # Вектори
        u = np.array([3.5, 1])  # Вектор u
        v = np.array([1, 3])  # Вектор v

        # Проєкція вектора v на u
        proj_v_on_u = (np.dot(v, u) / np.dot(u, u)) * u

        # Початкові точки
        origin = np.array([0, 0])

        # Малювання векторів
        draw_vector(origin, u, color='blue')
        draw_vector(origin, v, color='brown')
        draw_vector(origin, proj_v_on_u, color='red')

        print_label(origin + u, label=r"$u$", label_offset=(-0.3, 0.20))
        print_label(origin + v, label=r"$v$", label_offset=(-0.50, -0.10))
        print_label(origin + proj_v_on_u, label=r'$\mathrm{proj}_{{u}} {v}$', label_offset=(-0.20, -0.50))
        # Пунктирна лінія для з'єднання
        draw_line(v, proj_v_on_u, linestyle="--", linewidth=0.8)


    scene = Scene(
        coordinate_rect=(-1, -1, 4, 4),
        grid_show=True,
        base_axis_show=False,
        axis_show=True
    )
    scene.add_frames(frame1)
    scene.show()
