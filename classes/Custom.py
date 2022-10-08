from .Frame import Frame
from .Figure import Figure


class Custom(Figure):
    def __init__(self, width: int, height: int, wait: int = 3, wipe: bool = False):
        super().__init__(wait, wipe)
        self.width = width
        self.height = height
        self.current_frame = Frame.empty(width, height)

    def render(self):
        return self.current_frame

    def step(self):
        pass
