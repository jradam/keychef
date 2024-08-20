import winput as w
import os
import sys
from main.types import KeyCode
from main.dictionary import keys


# Required for pyinstaller to find files
def absolute_path(relative_path) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Get the KeyCode from a Dictionary Key tuple
def get_keycode(name: str) -> KeyCode:
    return keys[name][0]


def hit(key) -> None:
    w.press_key(key)
    w.release_key(key)
