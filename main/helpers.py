from winput import (
    press_key,
    release_key,
    VK_SHIFT,
    KeyboardEvent,
    WM_KEYDOWN,
    WM_KEYUP,
    VK_ESCAPE,
    WP_DONT_PASS_INPUT_ON,
)
import os
import sys


# Required for pyinstaller to find files
def absolute_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def hit(key):
    press_key(key)
    release_key(key)


def shift_hit(key):
    press_key(VK_SHIFT)
    hit(key)
    release_key(VK_SHIFT)


def press(key, shift=False):
    if shift == True:
        shift_hit(key)
    else:
        hit(key)


def remap(event: KeyboardEvent, from_key, to_key) -> bool:
    if event.vkCode == from_key:
        if event.action == WM_KEYDOWN:
            press_key(to_key)
        elif event.action == WM_KEYUP:
            release_key(to_key)
        return True
    return False
