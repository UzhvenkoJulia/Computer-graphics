from abc import abstractmethod, ABC


class AnimationListener(ABC):
    @abstractmethod
    def on_start(self, scene): pass

    @abstractmethod
    def on_finish(self, scene): pass

    @abstractmethod
    def on_repeat(self, scene): pass


class AnimationFinishedListener(AnimationListener, ABC):
    def on_start(self, scene): pass

    def on_repeat(self, scene): pass


class FinishCallback(AnimationFinishedListener):
    def __init__(self, callback):
        if callable(callback):
            self.callback = callback

    def on_finish(self, scene):
        self.callback(scene)
