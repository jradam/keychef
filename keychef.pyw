from main.settings import activate_key, on_activate
import time
from winput import (
    press_key,
    release_key,
    KeyboardEvent,
    hook_keyboard,
    wait_messages,
    WM_KEYUP,
    WM_KEYDOWN,
    WP_DONT_PASS_INPUT_ON,
    WP_STOP,
    WP_UNHOOK,
)
import winput as w
from main.helpers import absolute_path, hit, press, remap
import threading
import PIL.Image
from pystray import Icon, Menu, MenuItem


# TODO: Fix windows "Are you sure you want to run this?" warning
# TODO: First iteration of settings - just show console window
# TODO: Add option to show or hide settings/console on startup
# TODO: Extract all bindings to user settings, make it a json file
# TODO: Finish readme
# TODO: Mouse movement


class State:
    def __init__(self):
        self.running = True
        self.cooking = False
        self.shifted = False
        self.sending_replacement = False
        self.last_key_time = 0
        self.last_key = None

    def exit(self):
        self.running = False
        hit(w.VK_ESCAPE)  # Hit key to trigger callback, which then quits

    def toggle_cooking(self, event: KeyboardEvent):
        if event.action == WM_KEYDOWN:
            self.cooking = True
            press_key(on_activate)
        elif event.action == WM_KEYUP:
            self.cooking = False
            release_key(on_activate)
        return WP_DONT_PASS_INPUT_ON

    def toggle_shifted(self, event: KeyboardEvent):
        if event.action == WM_KEYDOWN:
            self.shifted = True
        elif event.action == WM_KEYUP:
            self.shifted = False

    def double(self, key1, key2):
        current_time = time.time()
        if self.last_key == key1[0] and (current_time - self.last_key_time) < 0.15:
            hit(w.VK_BACK)
            press(*key2)
        else:
            press(*key1)
        self.last_key_time = current_time
        self.last_key = key1[0]

    def send_replacement(self):
        self.sending_replacement = True
        hit(activate_key)
        self.sending_replacement = False


state = State()


def click(icon, item):
    if str(item) == "Exit":
        icon.stop()
        state.exit()


icon = Icon(
    "Keychef",
    PIL.Image.open(absolute_path("icon.png")),
    menu=Menu(MenuItem("Settings", click), MenuItem("Exit", click)),
)

# Start icon in separate thread
threading.Thread(target=icon.run).start()


def handle_ingredients(event: KeyboardEvent):
    key_map = {
        w.VK_F: lambda: state.double((w.VK_OEM_4, True), (w.VK_OEM_6, True)),
        w.VK_D: lambda: state.double((w.VK_9, True), (w.VK_0, True)),
        w.VK_S: lambda: state.double((w.VK_OEM_4, False), (w.VK_OEM_6, False)),
        w.VK_G: lambda: state.double((w.VK_OEM_MINUS, False), (w.VK_OEM_MINUS, True)),
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
        w.VK_CAPITAL: lambda: hit(w.VK_CAPITAL),
        w.VK_C: lambda: state.send_replacement(),
    }
    if event.action == WM_KEYDOWN:
        action = key_map.get(event.vkCode)
        if action:
            action()
            return WP_DONT_PASS_INPUT_ON


def callback(event: KeyboardEvent):
    if not state.running:
        return WP_UNHOOK | WP_STOP
    if state.cooking and event.vkCode == w.VK_Q:
        icon.stop()
        state.exit()
    if event.vkCode == w.VK_LSHIFT:
        return state.toggle_shifted(event)
    if (
        event.vkCode == activate_key
        and not state.shifted
        and not state.sending_replacement
    ):
        return state.toggle_cooking(event)
    if state.cooking:
        return handle_ingredients(event)
    if remap(event, w.VK_CAPITAL, w.VK_ESCAPE):
        return WP_DONT_PASS_INPUT_ON


hook_keyboard(callback)
wait_messages()
