from .dictionary import keys
from .keychef_types import KeyCode
import os
import sys
import winput as w


# Required for pyinstaller to find files
def absolute_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Get the KeyCode from a Dictionary Key tuple
def get_keycode(name: str) -> KeyCode:
    return keys[name][0]


def hit(key: int) -> None:
    w.press_key(key)
    w.release_key(key)
