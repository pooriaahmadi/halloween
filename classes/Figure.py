from .Frame import Frame


class Figure:
    def __init__(self, wait: int = 60, wipe: bool = False):
        self.wait = wait
        self.wipe = wipe
        self.current_frame = None

    def render(self) -> Frame:
        pass

    def step(self) -> None:
        pass
