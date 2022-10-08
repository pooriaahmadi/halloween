from .Frame import Frame
from .Figure import Figure
from typing import List


class Animated(Figure):
    def __init__(self, frames: List[Frame], wait: int = 300, wipe: bool = False):
        super().__init__(wait, wipe)
        self.frames = frames
        self.index = 0
        self.current_frame = self.frames[self.index]

    def render(self):
        return self.current_frame

    def step(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.index = 0

        self.current_frame = self.frames[self.index]
