from .Frame import Frame
from .Figure import Figure
from rpi_ws281x import Color
from typing import Dict, List
import os


def read_files(files: List[str]) -> Dict[str, Frame]:
    output: Dict[str, Frame] = {}
    for file in files:
        output[file.replace(".txt", "")] = Frame.load_from_file_matrix_numbers_custom(
            f"figures/letters/{file}", Color(255, 0, 0), 8, 8)

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
        
        if key == "text":
            total_length = 0
            for character in value:
                if character == " ":
                    total_length += 3
                    continue

                frame = self.LETTERS[character]
                total_length += frame.data_width + 1
            
            self.set_parameter("total_length", total_length)

        self.parameters[key] = value

    def render(self):
        return self.current_frame

    def total_length(self, index: int) -> int:
        output = 0
        for character in self.parameters["text"][0:index]:
            if character == " ":
                output += 3
                continue

            frame = self.LETTERS[character]
            output += frame.data_width + 1
        
        return output
    
    def step(self):
        self.current_frame.pixels = []
        if self.index >= self.parameters["total_length"]:
            self.index = -8
        
        for index, character in enumerate(self.parameters["text"]):
            if character == " ":
                frame = Frame.empty(8, 8)
            else:
                frame = self.LETTERS[character]
            self.current_frame.draw_frame_at_pos(
                frame, self.total_length(index) - self.index, 2)

        self.index += 1
