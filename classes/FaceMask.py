from rpi_ws281x import PixelStrip, Color
from .Frame import Frame
from .Rainbow import Rainbow
from .RainbowHorizontal import RainbowHorizontal
from .Custom import Custom
from .Animated import Animated
from .ScrollingText import ScrollingText
from .InstantText import InstantText
import time


class FaceMask:

    EFFECTS = {
        "vertical_rainbow": Rainbow(2),
        "horizontal_rainbow": RainbowHorizontal(2),
        "custom": Custom(8, 8),
        "get_out_the_way": Animated([Frame.load_from_file_matrix_numbers("figures/arrows/1.txt", Color(255, 0, 0)),
                                     Frame.load_from_file_matrix_numbers(
                                         "figures/arrows/2.txt", Color(255, 0, 0)),
                                     Frame.load_from_file_matrix_numbers(
                                         "figures/arrows/3.txt", Color(255, 0, 0)),
                                     Frame.load_from_file_matrix_numbers(
                                         "figures/arrows/4.txt", Color(255, 0, 0)),
                                     Frame.load_from_file_matrix_numbers(
                                         "figures/arrows/5.txt", Color(255, 0, 0)),
                                     Frame.load_from_file_matrix_numbers("figures/arrows/6.txt", Color(255, 0, 0))], wipe=True),
        "moon": Animated([Frame.load_from_file_matrix_numbers("figures/moon/1.txt", Color(27, 97, 209))]),
        "kiss": Animated([Frame.load_from_file_matrix_numbers("figures/smile/2.txt", Color(255, 0, 0))]),
        "w": Animated([Frame.load_from_file_matrix_numbers("figures/uwu/1.txt", Color(255, 48, 155))]),
        "uwu": Animated([Frame.load_from_file_matrix_numbers("figures/uwu/2.txt", Color(255, 48, 155))]),
        "smile": Animated([Frame.load_from_file_matrix_numbers("figures/smile/1.txt", Color(255, 255, 0))]),
        "smile2": Animated([Frame.load_from_file_matrix_numbers("figures/smile/3.txt", Color(255, 255, 0))]),
        "smile_animated": Animated([Frame.load_from_file_matrix_numbers("figures/smile/1.txt", Color(255, 255, 0)), Frame.load_from_file_matrix_numbers("figures/smile/3.txt", Color(255, 255, 0))], wait=1000, wipe=True),
        "neutral": Animated([Frame.load_from_file_matrix_numbers("figures/neutral/1.txt", Color(255, 255, 0))]),
        "heart": Animated([Frame.load_from_file_matrix_numbers("figures/heart/1.txt", Color(255, 0, 0))]),
        "ok": Animated([Frame.load_from_file_matrix_numbers("figures/words/ok.txt", Color(255, 0, 0))]),
        "no": Animated([Frame.load_from_file_matrix_numbers("figures/words/no.txt", Color(255, 0, 0))]),
        "pumpkin": Animated([Frame.load_from_colors([
            [0, 0, 0, Color(60, 196, 82), Color(60, 196, 82), 0, 0, 0],
            [0, 0, 0, 0, Color(60, 196, 82), 0, 0, 0],
            [0, Color(255, 100, 0), Color(255, 100, 0), Color(255, 100, 0), Color(
                255, 100, 0), Color(255, 100, 0), Color(255, 100, 0), 0],
            [Color(255, 100, 0), Color(255, 100, 0), Color(255, 255, 0), Color(
                255, 100, 0), Color(255, 100, 0), Color(255, 255, 0), Color(255, 100, 0), Color(255, 100, 0)],
            [Color(255, 100, 0), Color(255, 255, 0), Color(255, 255, 0), Color(
                255, 100, 0), Color(255, 100, 0), Color(255, 255, 0), Color(255, 255, 0), Color(255, 100, 0)],
            [Color(255, 100, 0), Color(255, 100, 0), Color(255, 100, 0), Color(255, 100, 0), Color(
                255, 100, 0), Color(255, 100, 0), Color(255, 100, 0), Color(255, 100, 0)],
            [Color(255, 100, 0), Color(255, 100, 0),  Color(255, 255, 0),  Color(255, 255, 0),  Color(
                255, 255, 0),  Color(255, 255, 0), Color(255, 100, 0), Color(255, 100, 0)],
            [0, Color(255, 100, 0), Color(255, 100, 0), Color(255, 255, 0), Color(
                255, 255, 0), Color(255, 100, 0), Color(255, 100, 0)]
        ], 8)]),
        "scrolling_text": ScrollingText(8, 8, 200, True),
        "instant_text": InstantText(8, 8, 500, True),
        "hi": Animated([Frame.load_from_file_matrix_numbers("figures/words/hi.txt", Color(255, 0, 0))]),
    }

    def __init__(self, pin: int, count: int, frequency: int, dma: int, brightness: int, invert: bool, channel: int, fps: int = 60):
        self.pin = pin
        self.count = count
        self.frequency = frequency
        self.dma = dma
        self.brightness = brightness
        self.invert = invert
        self.channel = channel
        self.running = False
        self.strip = PixelStrip(count, pin, frequency,
                                dma, invert, brightness, channel)
        self.strip.begin()
        self.color_wipe(Color(0, 0, 0), 0)
        self.__current_effect = self.EFFECTS["scrolling_text"]
        self.fps = fps
        self.clients = []

    @property
    def current_effect(self):
        return self.__current_effect

    @current_effect.setter
    def current_effect(self, value):
        self.color_wipe(Color(0, 0, 0), 0)
        self.__current_effect = value

    def color_wipe(self, color: Color, wait_ms: int) -> None:
        """Wipe color across display a pixel at a time"""
        if wait_ms == 0:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()
            return

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def draw_frame(self, frame: Frame):
        frame.draw(self.strip)

    def run(self):
        self.running = True
        while self.running:
            if not self.current_effect:
                continue
            if self.current_effect.wipe:
                self.color_wipe(Color(0, 0, 0), 0)

            self.current_effect.render().draw(self.strip)
            self.current_effect.step()

            time.sleep(self.current_effect.wait / 1000.0)
