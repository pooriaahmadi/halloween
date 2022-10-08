from rpi_ws281x import Color, PixelStrip

class Pixel:
    def __init__(self, index: int, color: Color):
        self.index = index
        self.color = color

    def draw(self, strip: PixelStrip):
        strip.setPixelColor(self.index, self.color)