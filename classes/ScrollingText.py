from .Frame import Frame
from .Figure import Figure
from rpi_ws281x import Color
from typing import List
import os


def read_files(self, files) -> List[Frame]:
    output: List[Frame] = []
    for file in files:
        output.append(Frame.load_from_file_matrix_numbers(
            file, Color(255, 0, 0)))


class ScrollingText(Figure):
    index: int = 0
    LETTERS = read_files([f for f in os.listdir(
        "figures/letters") if os.path.isfile(os.path.join("figures/letters", f))])

    def __init__(self, width: int, height: int, wait: int = 3, wipe: bool = False):
        super().__init__(wait, wipe)
        self.width = width
        self.height = height
        self.current_frame = Frame.empty(width, height)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def test(self, new_text: str) -> None:
        self.__text = new_text

    def render(self):
        return self.current_frame

    def step(self):

        self.index += 1
