import time
import pystray
import PIL.Image
import winput as w
import sys
import os
import threading


def absolute_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# TODO: Create requirements.txt file
# TODO: First iteration of settings - just show console window
# TODO: Instead of `running`, `shifted`, etc, use a class to store state
# TODO: Finish extracting all bindings to user settings
# TODO: Finish readme
# TODO: Change caps lock to escape
# TODO: Add caps lock functionality to other key
# TODO: Mouse movement
# TODO: Add a build process to .exe
# TODO: Binding Caps Lock
# TODO: Add a gui?


# USER SETTINGS HERE
activate_key = w.VK_OEM_1
on_activate = w.VK_F13


# TRAY ICON


def on_clicked(icon, item):
    if str(item) == "Settings":
        global settings
        # Open settings...
    elif str(item) == "Exit":
        global running
        running = False
        icon.stop()


image = PIL.Image.open(absolute_path("icon.png"))
running = True

icon = pystray.Icon(
    "Keychef",
    image,
    menu=pystray.Menu(
        pystray.MenuItem("Settings", on_clicked), pystray.MenuItem("Exit", on_clicked)
    ),
)


# Start icon in separate thread
threading.Thread(target=icon.run).start()


# KEYCHEF
cooking, shifted, sending_replacement = False, False, False
last_key_time, last_key = 0, None


def toggle_cooking(event: w.KeyboardEvent):
    global cooking
    if event.action == w.WM_KEYDOWN:
        cooking = True
        w.press_key(on_activate)
    elif event.action == w.WM_KEYUP:
        cooking = False
        w.release_key(on_activate)
    return w.WP_DONT_PASS_INPUT_ON


def toggle_shifted(event: w.KeyboardEvent):
    global shifted
    if event.action == w.WM_KEYDOWN:
        shifted = True
    elif event.action == w.WM_KEYUP:
        shifted = False


def hit(key):
    w.press_key(key)
    w.release_key(key)


def shift_hit(key):
    w.press_key(w.VK_SHIFT)
    hit(key)
    w.release_key(w.VK_SHIFT)


def press(key, shift=False):
    if shift == True:
        shift_hit(key)
    else:
        hit(key)


def double(key1, key2):
    global last_key_time, last_key
    current_time = time.time()
    if last_key == key1[0] and (current_time - last_key_time) < 0.15:
        hit(w.VK_BACK)
        press(*key2)
    else:
        press(*key1)
    last_key_time = current_time
    last_key = key1[0]


def send_replacement():
    global sending_replacement
    sending_replacement = True
    hit(activate_key)
    sending_replacement = False


def handle_ingredients(event: w.KeyboardEvent):
    global sending_replacement
    key_map = {
        w.VK_F: lambda: double((w.VK_OEM_4, True), (w.VK_OEM_6, True)),
        w.VK_D: lambda: double((w.VK_9, True), (w.VK_0, True)),
        w.VK_S: lambda: double((w.VK_OEM_4, False), (w.VK_OEM_6, False)),
        w.VK_G: lambda: double((w.VK_OEM_MINUS, False), (w.VK_OEM_MINUS, True)),
        w.VK_A: lambda: press(w.VK_7, True),
        w.VK_M: lambda: press(w.VK_4, True),
        w.VK_I: lambda: press(w.VK_2, True),
        w.VK_E: lambda: press(w.VK_OEM_PLUS),
        w.VK_N: lambda: press(w.VK_RETURN),
        w.VK_SPACE: lambda: press(w.VK_BACK),
        w.VK_X: lambda: press(w.VK_DELETE),
        w.VK_H: lambda: press(w.VK_LEFT),
        w.VK_J: lambda: press(w.VK_DOWN),
        w.VK_K: lambda: press(w.VK_UP),
        w.VK_L: lambda: press(w.VK_RIGHT),
        w.VK_C: lambda: send_replacement(),
    }
    if event.action == w.WM_KEYDOWN:
        action = key_map.get(event.vkCode)
        if action:
            action()
            return w.WP_DONT_PASS_INPUT_ON


def keyboard_callback(event: w.KeyboardEvent):
    global running
    if not running:
        return w.WP_UNHOOK | w.WP_STOP
    if event.vkCode == w.VK_LSHIFT:
        return toggle_shifted(event)
    if event.vkCode == activate_key and not shifted and not sending_replacement:
        return toggle_cooking(event)
    elif cooking:
        return handle_ingredients(event)


w.hook_keyboard(keyboard_callback)
w.wait_messages()
