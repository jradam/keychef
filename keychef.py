from main.settings import (
    activate_key,
    on_activate,
    replace_key,
    layer_binds,
    permanent_binds,
)
from main.dictionary import keys
from winput import (
    WM_KEYUP,
    WM_KEYDOWN,
    WP_DONT_PASS_INPUT_ON,
    WP_STOP,
    WP_UNHOOK,
)
import winput as w
from main.helpers import hit, press, get_keycode
from main.icon import setup_icon
import threading

# TODO: Simplify the callback
# TODO: Add quit hotkey to user settings
# TODO: Mouse movement
# TODO: Make settings a json file
# TODO: Dictionary currently for UK layout. Can detect layout?
# TODO: First iteration of settings - just show console window
# TODO: Add option to show or hide settings/console on startup


class State:
    def __init__(self):
        self.running: bool = True
        self.cooking: bool = False
        self.shifted: bool = False
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


state = State()


def handle_ingredients(event, binds):
    if event.action == WM_KEYDOWN:
        for bind in binds:
            if event.vkCode == get_keycode(bind["key"]):
                output_key, output_shift = keys[bind["output"]]
                press(output_key, output_shift)
                return WP_DONT_PASS_INPUT_ON
    return None


def callback(event: w.KeyboardEvent) -> int | None:
    if not state.running:
        return WP_UNHOOK | WP_STOP

    if state.cooking and event.vkCode == w.VK_Q:
        icon.stop()
        state.exit()
        return

    if event.vkCode == w.VK_LSHIFT:
        return state.toggle_shifted(event)

    if state.cooking:
        if event.action == WM_KEYDOWN:
            if event.vkCode == get_keycode(replace_key):
                hit(activate_key)
                return WP_DONT_PASS_INPUT_ON
            else:
                return handle_ingredients(event, layer_binds)

    if event.vkCode == activate_key and not state.shifted:
        return state.toggle_cooking(event)

    return handle_ingredients(event, permanent_binds)


def main() -> None:
    global icon
    icon = setup_icon(state)
    # Start icon in separate thread
    threading.Thread(target=icon.run).start()

    w.hook_keyboard(callback)
    w.wait_messages()


if __name__ == "__main__":
    main()
