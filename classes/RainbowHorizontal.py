from .Rainbow import Rainbow
from .Frame import Frame


class RainbowHorizontal(Rainbow):
    def render(self) -> Frame:
        frame = Frame.empty(8, 8)

        for index, color in enumerate(self.get_current_colors()):
            if index * self.colors_width < frame.width:
                for times in range(self.colors_width):
                    frame.draw_horizontal_line(
                        index * self.colors_width + times, color)

        self.current_frame = frame
        return frame
