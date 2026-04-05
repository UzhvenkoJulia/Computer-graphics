from abc import ABCMeta, abstractmethod


class Frame(metaclass=ABCMeta):

    @abstractmethod
    def on_frame(self, scene):
        pass


class FrameCallback(Frame):
    def __init__(self, callback):
        if callable(callback):
            self.callback = callback

    def on_frame(self, scene):
        self.callback(scene)
