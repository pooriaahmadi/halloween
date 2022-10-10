from .Frame import Frame


class Figure:
    parameters = {}

    def __init__(self, wait: int = 60, wipe: bool = False):
        self.wait = wait
        self.wipe = wipe
        self.current_frame = None

    def set_parameter(self, key: str, value):
        self.parameters[key] = value

    def render(self) -> Frame:
        pass

    def step(self) -> None:
        pass
