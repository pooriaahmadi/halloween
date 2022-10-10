import json
from typing import Dict, List
from flask import Flask, render_template, request
from classes import FaceMask
import config
from rpi_ws281x import Color
from threading import Thread

app = Flask(__name__)
facemask = FaceMask(config.LED["PIN"], config.LED["COUNT"], config.LED["FREQUENCY"],
                    config.LED["DMA"], config.LED["BRIGHTNESS"], config.LED["INVERT"], config.LED["CHANNEL"])
# test_frame = Frame.load_from_file_matrix_numbers(
#     "figures/neutral/1.txt", Color(255, 0, 0))
# facemask.draw_frame(test_frame)
facemask_thread = Thread(target=facemask.run)


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/custom")
def custom():
    return render_template("custom.html")


@app.route("/text")
def text():
    return render_template("text.html")


@app.route("/api/leds")
def current_frame():
    if not facemask.current_effect or not facemask.current_effect.current_frame:
        return {"pixels": []}

    pixels: List[Dict] = []
    color = Color(255, 255, 255)
    color.as_integer_ratio()
    if facemask.current_effect.current_frame:
        for pixel in facemask.current_effect.current_frame.pixels:
            pixels.append({
                "index": pixel.index,
                "color": pixel.color
            })

    return {
        "width": facemask.current_effect.current_frame.width,
        "height": facemask.current_effect.current_frame.height,
        "pixels": pixels,
        "brightness": facemask.brightness
    }


@app.post("/api/leds/<int:id>")
def set_led(id: int):
    color = request.json["color"].split(",")
    color = Color(int(color[0]), int(color[1]), int(color[2]))
    facemask.current_effect = facemask.EFFECTS["custom"]
    facemask.current_effect.current_frame.add_led(id, color)

    return {
        "message": "done"
    }


@app.delete("/api/leds/<int:id>")
def delete_led(id: int):
    facemask.current_effect = facemask.EFFECTS["custom"]
    for index, pixel in enumerate(facemask.current_effect.current_frame.pixels):
        if pixel.index == id:
            del facemask.current_effect.current_frame.pixels[index]

    return {
        "message": "done"
    }


@app.post("/api/brightness/<int:value>")
def set_brightness(value: int):
    facemask.strip.setBrightness(value)
    facemask.brightness = value

    return {
        "message": "done"
    }


@app.get("/api/brightness/")
def get_brightness():
    return str(facemask.brightness)


@app.post("/api/effects/<int:index>")
def set_effect(index: int):
    keys = list(facemask.EFFECTS.keys())
    if index >= len(keys) or index < 0:
        return {
            "message": "index doesn't exist"
        }, 404

    facemask.current_effect = facemask.EFFECTS[keys[index]]
    return {
        "message": "done"
    }


@app.get("/api/effects/")
def get_effects():
    keys = facemask.EFFECTS.keys()
    return list(keys)


@app.get("/api/effects/current")
def get_current_effect():
    return str(list(facemask.EFFECTS.values()).index(facemask.current_effect))


@app.get("/api/effects/current/parameters")
def effect_parameters_get():
    return facemask.current_effect.parameters


@app.post("/api/effects/current/parameters/<string:key>")
def effect_parameters_set(key):
    facemask.current_effect.set_parameter(key, request.json["data"])
    return facemask.current_effect.parameters


facemask_thread.setDaemon(True)
facemask_thread.start()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
