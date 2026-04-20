from src.engine.model.SimplePolygon import SimplePolygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4, vertex

if __name__ == '__main__':
    RECT_KEY = "rect"
    O = vertex(0, 0, 0)
    t1 = Vec4(1, 0, 0)
    t2 = Vec4(1, 1, 0)
    t3 = Vec4(0, 1, 0)


    class SimplePolygonScene(AnimatedScene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            polygon = SimplePolygon(
                                    O,
                                    O + t1,
                                    O + t2,
                                    O + t3,
                                    edgecolor="red",
                                    )
            self[RECT_KEY] = polygon
            polygon.show_local_frame()
            print(polygon.transformed_geometry)


    animated_scene = SimplePolygonScene(
        coordinate_rect=(0, 0, 0, 2, 2, 2)
    )


    def frame1(scene):
        pass


    def frame2(scene):
        scene[RECT_KEY].transformation = Mat4x4.translation(1, 1, 0)


    animated_scene.add_frames(frame1, frame2)
    animated_scene.show()
