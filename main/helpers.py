import winput as w
from winput import (
    VK_SHIFT,
    WM_KEYDOWN,
    WM_KEYUP,
)
import os
import sys


# Required for pyinstaller to find files
def absolute_path(relative_path) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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


def remap(event: w.KeyboardEvent, from_key, to_key) -> bool:
    if event.vkCode == from_key:
        if event.action == WM_KEYDOWN:
            w.press_key(to_key)
        elif event.action == WM_KEYUP:
            w.release_key(to_key)
        return True
    return False
