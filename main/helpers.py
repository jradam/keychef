import winput as w
from winput import (
    VK_SHIFT,
    WM_KEYDOWN,
    WM_KEYUP,
)
import os
import sys
from main.types import KeyCode
from main.dictionary import keys


# Required for pyinstaller to find files
def absolute_path(relative_path) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_keycode(name: str) -> KeyCode:
    return keys[name][0]


def hit(key) -> None:
    w.press_key(key)
    w.release_key(key)


def shift_hit(key) -> None:
    w.press_key(VK_SHIFT)
    hit(key)
    w.release_key(VK_SHIFT)


def press(key, shift=False) -> None:
    if shift == True:
        shift_hit(key)
    else:
        hit(key)
