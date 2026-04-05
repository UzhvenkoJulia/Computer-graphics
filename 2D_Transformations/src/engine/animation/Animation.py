from abc import ABC, abstractmethod

from src.engine.animation.AnimationListener import AnimationListener, FinishCallback
from src.math.Mat3x3 import Mat3x3

ANIMATION_STOPPED = "ANIMATION_STOPED"
ANIMATION_PLAYED = "ANIMATION_FINISHED"


class Animation(ABC):

    def __init__(self,
                 end,  # Кінцеве значення трасформації
                 channel="default",  # ідентифікатор фігури до якої має застосовуватися анімація
                 frames=60,  # Кількість кадрів анімації 60 (при інтервалі 16 мілісекунд буде 1 секунда)
                 interval=16,  # Час в мілісекундах між кадрами анімації
                 repeat=False,  # Чи циклічна анімація
                 apply_geometry_transformation_on_finish=False,  # Чи трансформує анімація всі вертекси на фініші
                 animation_listener=None,  # спостерігач
                 ):
        self.start = Mat3x3.identity()
        self.end = end
        self.channel = channel
        self.frames = frames
        self.interval = interval
        self.repeat = repeat
        self.state = ANIMATION_STOPPED
        self.__animation_listeners = []

        self.add_animation_listener(animation_listener)

        if apply_geometry_transformation_on_finish:
            def apply_transformation_callback(animated_scene):
                print("Applied transformation to geometry")
                animated_scene[self.channel].apply_transformation_to_geometry()

            self.add_animation_listener(apply_transformation_callback)

    def add_animation_listener(self, animation_listener):
        if animation_listener is not None:
            if isinstance(animation_listener, AnimationListener):
                self.__animation_listeners.append(animation_listener)
            elif callable(animation_listener):
                self.__animation_listeners.append(FinishCallback(animation_listener))

    def notify(self, scene, frame):
        if frame == 0:
            if self.state == ANIMATION_STOPPED:
                self.state = ANIMATION_PLAYED
                for listener in self.__animation_listeners:
                    listener.on_start(scene)

        if frame == self.frames - 1:
            if self.state == ANIMATION_PLAYED:
                if self.repeat:
                    for listener in self.__animation_listeners:
                        listener.on_repeat(scene)
                else:
                    self.state = ANIMATION_STOPPED
                    for listener in self.__animation_listeners:
                        listener.on_finish(scene)

    @abstractmethod
    def current_transformation(self, frame):
        pass
