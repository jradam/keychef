import time
from typing import Tuple
import winput as w
from main.helpers import hit, press


DOUBLE_TAP_SPEED: float = 0.15
last_key_time: float = 0
last_key: int | None = None


def double(key1: Tuple[int, bool], key2: Tuple[int, bool]) -> None:
    global last_key_time, last_key
    current_time = time.time()
    if last_key == key1[0] and (current_time - last_key_time) < DOUBLE_TAP_SPEED:
        hit(w.VK_BACK)
        press(*key2)
    else:
        press(*key1)
    last_key_time = current_time
    last_key = key1[0]
