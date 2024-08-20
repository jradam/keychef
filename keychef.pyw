from main.settings import activate_key, on_activate
from winput import (
    WM_KEYUP,
    WM_KEYDOWN,
    WP_DONT_PASS_INPUT_ON,
    WP_STOP,
    WP_UNHOOK,
)
import winput as w
from main.helpers import hit, press, remap
from main.double import double
from main.icon import setup_icon
import threading


# TODO: Fix windows "Are you sure you want to run this?" warning
# TODO: Make hold space work as shift
# TODO: First iteration of settings - just show console window
# TODO: Add option to show or hide settings/console on startup
# TODO: Extract all bindings to user settings, make it a json file
# TODO: Finish readme
# TODO: Mouse movement


class State:
    def __init__(self):
        self.running: bool = True
        self.cooking: bool = False
        self.shifted: bool = False
        self.sending_replacement: bool = False
        self.last_key_time: float = 0
        self.last_key: int | None = None

    def exit(self) -> None:
        self.running = False
        hit(w.VK_ESCAPE)  # Hit key to trigger callback, which then quits

    def toggle_cooking(self, event: w.KeyboardEvent) -> int:
        if event.action == WM_KEYDOWN:
            self.cooking = True
            w.press_key(on_activate)
        elif event.action == WM_KEYUP:
            self.cooking = False
            w.release_key(on_activate)
        return WP_DONT_PASS_INPUT_ON

    def toggle_shifted(self, event: w.KeyboardEvent) -> None:
        if event.action == WM_KEYDOWN:
            self.shifted = True
        elif event.action == WM_KEYUP:
            self.shifted = False

    def send_replacement(self) -> None:
        self.sending_replacement = True
        hit(activate_key)
        self.sending_replacement = False


state = State()


def handle_ingredients(event: w.KeyboardEvent) -> int | None:
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
        w.VK_CAPITAL: lambda: hit(w.VK_CAPITAL),
        w.VK_C: lambda: state.send_replacement(),
    }
    if event.action == WM_KEYDOWN:
        action = key_map.get(event.vkCode)
        if action:
            action()
            return WP_DONT_PASS_INPUT_ON


def callback(event: w.KeyboardEvent) -> int | None:
    if not state.running:
        return WP_UNHOOK | WP_STOP

    if state.cooking and event.vkCode == w.VK_Q:
        icon.stop()
        state.exit()
        return

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


def main() -> None:
    global icon
    icon = setup_icon(state)
    # Start icon in separate thread
    threading.Thread(target=icon.run).start()

    w.hook_keyboard(callback)
    w.wait_messages()


if __name__ == "__main__":
    main()
