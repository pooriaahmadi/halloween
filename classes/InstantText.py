from .ScrollingText import ScrollingText
from .Frame import Frame
from rpi_ws281x import Color


class InstantText(ScrollingText):
    words = []

    def __init__(self, width: int, height: int, wait: int = 3, wipe: bool = False):
        super().__init__(width, height, wait, wipe)
        self.set_parameter("text", "hi 5")

    def set_parameter(self, key: str, value):
        if key == "color" and not isinstance(value, int):
            self.parameters[key] = Color(
                int(value[0]), int(value[1]), int(value[2]))
            for letter in self.LETTERS.values():
                letter.change_color(self.parameters[key])
            return
        if key == "text":
            self.words = value.split(" ")
        self.parameters[key] = value

    def step(self):
        self.current_frame.pixels = []
        if self.index >= len(self.words):
            self.index = 0

        for index, character in enumerate(self.words[self.index]):
            if character == " ":
                frame = Frame.empty(8, 8)
            else:
                frame = self.LETTERS[character]

            self.current_frame.draw_frame_at_pos(
                frame, self.total_length(index), 2)

        self.index += 1
