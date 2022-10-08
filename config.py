import os
from dotenv import load_dotenv
from typing import Dict
load_dotenv()

PORT: int = int(os.getenv("PORT"))
HOST: str = os.getenv("HOST")
DEBUG: bool = True if os.getenv("DEBUG") == "1" else False
LED: Dict = {
    "COUNT": int(os.getenv("LED_COUNT")),
    "PIN": int(os.getenv("LED_PIN")),
    "FREQUENCY": int(os.getenv("LED_FREQ_HZ")),
    "DMA": int(os.getenv("LED_DMA")),
    "BRIGHTNESS": int(os.getenv("LED_BRIGHTNESS")),
    "INVERT": True if os.getenv("LED_INVERT") == "1" else False,
    "CHANNEL": int(os.getenv("LED_CHANNEL"))
}
