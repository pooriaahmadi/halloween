from rpi_ws281x import Color, PixelStrip
from .Frame import Frame
from .Figure import Figure
from typing import List


class Rainbow(Figure):
    COLORS = [
        Color(255, 0, 0),
        Color(255, 30, 0),
        Color(255, 59, 0),
        Color(255, 94, 0),
        Color(255, 128, 0),
        Color(255, 160, 0),
        Color(255, 192, 0),
        Color(255, 223, 0),
        Color(255, 255, 0),
        Color(223, 255, 0),
        Color(192, 255, 0),
        Color(160, 255, 0),
        Color(128, 255, 0),
        Color(96, 255, 0),
        Color(64, 255, 0),
        Color(32, 255, 0),
        Color(0, 255, 0),
        Color(0, 255, 31),
        Color(0, 255, 63),
        Color(0, 255, 94),
        Color(0, 255, 128),
        Color(0, 255, 160),
        Color(0, 255, 192),
        Color(0, 255, 223),
        Color(0, 255, 255),
        Color(0, 222, 255),
        Color(0, 189, 255),
        Color(0, 158, 255),
        Color(0, 128, 255),
        Color(0, 96, 255),
        Color(0, 64, 255),
        Color(0, 32, 255),
        Color(0, 0, 255),
        Color(32, 0, 255),
        Color(64, 0, 255),
        Color(96, 0, 255),
        Color(128, 0, 255),
        Color(160, 0, 255),
        Color(192, 0, 255),
        Color(223, 0, 255),
        Color(255, 0, 255),
        Color(255, 0, 223),
        Color(255, 0, 192),
        Color(255, 0, 160),
        Color(255, 0, 128),
        Color(255, 0, 90),
        Color(255, 0, 37),
        Color(255, 0, 20),
    ]

    def __init__(self, colors_width: int, wait: int = 60, wipe: bool = False):
        super().__init__(wait, wipe)
        self.colors_width = colors_width
        self.offset_x = 0

    def get_current_colors(self) -> List[Color]:
        output = self.COLORS.copy()
        for _ in range(self.offset_x):
            color = output.pop()
            output.insert(0, color)

        return output

    def step(self):
        self.offset_x += 1
        if self.offset_x > len(self.COLORS):
            self.offset_x = 1

    def render(self) -> Frame:
        frame = Frame.empty(8, 8)

        for index, color in enumerate(self.get_current_colors()):
            if index * self.colors_width < frame.width:
                for times in range(self.colors_width):
                    frame.draw_vertical_line(
                        index * self.colors_width + times, color)

        self.current_frame = frame
        return frame
