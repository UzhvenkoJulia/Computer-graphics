import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

class Task1Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square_initial = Polygon(color="blue", line_style="--", vertices_show=True)
        square_initial.set_geometry(
            0, 0,
            1, 0,
            1, 1,
            0, 1
        )
        self["initial_square"] = square_initial

        square_final = Polygon(color="red", line_style="-", vertices_show=True)
        # координати розраховано самостійно математично
        square_final.set_geometry(
            2, 3,
            2.866, 3.5,
            2.366, 4.366,
            1.5, 3.866
        )
        self["final_square"] = square_final

if __name__ == '__main__':
    scene = Task1Scene(
        image_size=(6, 6),                 
        coordinate_rect=(-1, -1, 5, 5),    
        title="Завдання 1: Композиція трансформацій",
        grid_show=True,                    
        axis_show=True                     
    )
    scene.show()