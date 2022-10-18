from __future__ import annotations
from rpi_ws281x import Color, PixelStrip
from typing import List, Union
from .Pixel import Pixel


class Frame:
    def __init__(self, pixels: List[Pixel], width: int = None, height: int = None):
        self.pixels = pixels
        self.width = width
        self.height = height
        self.data_width = None
        self.data_height = None

    def draw(self, strip: PixelStrip) -> None:
        for pixel in self.pixels:
            pixel.draw(strip)
        strip.show()

    def change_color(self, color: Color) -> None:
        for index in range(len(self.pixels)):
            self.pixels[index].color = color

    def draw_vertical_line(self, column: int, color: Color) -> None:
        for i in range(self.height):
            offset = column if i % 2 == 0 else self.width - column - 1
            self.pixels.append(Pixel(i * self.width + offset, color))

    def draw_horizontal_line(self, row: int, color: Color) -> None:
        for i in range(self.width):
            self.pixels.append(Pixel(row * self.height + i, color))

    def draw_frame_at_pos(self, frame: Frame, x: int, y: int) -> None:
        for pixel in frame.pixels:
            index = pixel.index + y * self.width
            if pixel.index // 8 % 2 == 0:
                if index // 8 == (index - x) // 8:
                    index -= x
                    self.pixels.append(Pixel(index, pixel.color))
            else:
                if index // 8 == (index + x) // 8:
                    index += x
                    self.pixels.append(Pixel(index, pixel.color))

    def add_led(self, id: int, color: Color):
        self.pixels.append(Pixel(id, color))

    @staticmethod
    def empty(width: int, height: int) -> Frame:
        return Frame([], width, height)

    @staticmethod
    def load_from_file_matrix_numbers(path: str, color: Color) -> Frame:
        file = open(path, "r")
        raw_data = file.read().split("\n")
        height = len(raw_data)
        width = len(raw_data[0])
        file.close()

        parsed_data = []
        for line in raw_data:
            parsed_line = []
            for character in line:
                parsed_line.append(int(character))

            parsed_data.append(parsed_line)

        return Frame.load_from_matrix_numbers(parsed_data, color, width, height)
    
    @staticmethod
    def load_from_file_matrix_numbers_custom(path: str, color: Color, width, height) -> Frame:
        file = open(path, "r")
        raw_data = file.read().split("\n")
        data_height = len(raw_data)
        data_width = len(raw_data[0])
        for index, line in enumerate(raw_data):
            raw_data[index] += "0"*(width - data_width)
        for i in range(height - data_height):
            raw_data.append("0"*width)
        file.close()

        parsed_data = []
        for line in raw_data:
            parsed_line = []
            for character in line:
                parsed_line.append(int(character))

            parsed_data.append(parsed_line)

        frame = Frame.load_from_matrix_numbers(parsed_data, color, width, height)
        frame.data_width = data_width
        frame.data_height = data_height
        return frame

    @staticmethod
    def load_from_matrix_numbers(data: List[List[int]], color: Color, width: int, height: int) -> Frame:
        output: List[Color] = []
        data_tmp = []
        for index, tmp in enumerate(data):
            if index % 2 == 0:
                tmp.reverse()
            data_tmp += tmp

        for index, pixel in enumerate(data_tmp):
            if pixel:
                output.append(Pixel(index, color))

        return Frame(output, width, height)

    @staticmethod
    def load_from_colors(data: List[List[Color]], height: int) -> Frame:
        output: List[Color] = []
        for index, color in enumerate(data):
            if isinstance(color, List):
                for index_, color_ in enumerate(color):
                    if color_ == 0:
                        continue
                    output.append(Pixel(index * height + index_, color_))
                continue

            if color == 0:
                continue
            output.append(Pixel(index, color))

        return Frame(output)
