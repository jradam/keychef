from winput import press_key, release_key, VK_SHIFT
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
