from flask import Flask
from classes import FaceMask, Frame
from rpi_ws281x import Color
from threading import Thread
from classes.Rainbow import Rainbow
import config

app = Flask(__name__)
facemask = FaceMask(config.LED["PIN"], config.LED["COUNT"], config.LED["FREQUENCY"],
                    config.LED["DMA"], config.LED["BRIGHTNESS"], config.LED["INVERT"], config.LED["CHANNEL"])

facemask.run()
# figure = Figure.load_from_file_matrix_numbers(
#     "figures/neutral/1.txt",
#     Color(100, 150, 0)
# )
# facemask.draw_figure(figure)

# figure = Figure.empty(8, 8)
# figure.draw_vertical_line(1, Color(255, 0, 0))
# figure.draw_horizontal_line(1, Color(0, 255, 0))
# figure.draw(facemask.strip)

# facemask.run()

# facemask_thread = Thread(target=facemask.run, daemon=True)
# facemask_thread.start()


# @app.route("/")
# def hello_world():
#     return "Hello world!"


# app.run(config.HOST, config.PORT)
