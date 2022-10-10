from .Frame import Frame
from .Figure import Figure
from rpi_ws281x import Color
from typing import Dict, List
import os


def read_files(files: List[str]) -> Dict[str, Frame]:
    output: Dict[str, Frame] = {}
    for file in files:
        output[file.replace(".txt", "")] = Frame.load_from_file_matrix_numbers(
            f"figures/letters/{file}", Color(255, 0, 0))

    return output


class ScrollingText(Figure):
    index: int = 0
    LETTERS: Dict[str, Frame] = read_files([f for f in os.listdir(
        "figures/letters") if os.path.isfile(os.path.join("figures/letters", f))])

    def __init__(self, width: int, height: int, wait: int = 3, wipe: bool = False):
        super().__init__(wait, wipe)
        self.width = width
        self.height = height
        self.current_frame = Frame.empty(width, height)
        self.set_parameter("text", "pooria")
        self.set_parameter("color", Color(255, 0, 0))

    def set_parameter(self, key: str, value):
        if key == "color" and not isinstance(value, int):
            self.parameters[key] = Color(
                int(value[0]), int(value[1]), int(value[2]))
            for letter in self.LETTERS.values():
                letter.change_color(self.parameters[key])
            return

        self.parameters[key] = value

    def render(self):
        return self.current_frame

    def step(self):
        self.current_frame.pixels = []
        if self.index // 5 >= len(self.parameters["text"]):
            self.index = -8

        for index, character in enumerate(self.parameters["text"]):
            frame = self.LETTERS[character]
            self.current_frame.draw_frame_at_pos(
                frame, index * 5 - self.index, 2)

        self.index += 1
