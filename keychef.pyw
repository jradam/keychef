from main.settings import (
    activate_key,
    exit_key,
    layer_binds,
    on_activate,
    permanent_binds,
    replace_key,
)
from main.dictionary import keys
from winput import (
    VK_SHIFT,
    WM_KEYDOWN,
    WM_KEYUP,
    WP_DONT_PASS_INPUT_ON,
    WP_STOP,
    WP_UNHOOK,
)
import winput as w
from main.helpers import hit, get_keycode
from main.icon import setup_icon
import threading

# TODO: Mouse movement
# TODO: Make settings a json file
# TODO: Dictionary currently for UK layout. Can detect layout?
# TODO: First iteration of settings - just show console window
# TODO: Add option to show or hide settings/console on startup


class State:
    def __init__(self):
        self.running: bool = True
        self.layer_active: bool = False
        self.shifted: bool = False
        self.sending_replacement: bool = False

    def exit(self) -> None:
        self.running = False
        hit(w.VK_ESCAPE)  # Hit key to trigger callback, which then quits

    def toggle_layer(self, event: w.KeyboardEvent) -> int:
        if event.action == WM_KEYDOWN:
            self.layer_active = True
            w.press_key(get_keycode(on_activate))
        elif event.action == WM_KEYUP:
            self.layer_active = False
            w.release_key(get_keycode(on_activate))
        return WP_DONT_PASS_INPUT_ON

    def toggle_shifted(self, event: w.KeyboardEvent) -> None:
        if event.action == WM_KEYDOWN:
            self.shifted = True
        elif event.action == WM_KEYUP:
            self.shifted = False

    def send_replacement(self):
        self.sending_replacement = True
        hit(get_keycode(activate_key))
        self.sending_replacement = False
        return WP_DONT_PASS_INPUT_ON


state = State()


def handle_layer(event, binds):
    for bind in binds:
        if event.vkCode == get_keycode(bind["key"]):
            output_key, output_shift = keys[bind["output"]]

            if event.action == WM_KEYDOWN:
                if output_shift:
                    w.press_key(VK_SHIFT)
                w.press_key(output_key)

            if event.action == WM_KEYUP:
                if output_shift:
                    w.release_key(VK_SHIFT)
                w.release_key(output_key)

            return WP_DONT_PASS_INPUT_ON


def callback(event: w.KeyboardEvent) -> int | None:
    if not state.running:
        return WP_UNHOOK | WP_STOP

    if state.layer_active and event.vkCode == get_keycode(exit_key):
        icon.stop()
        state.exit()
        return

    # If shift is pressed, return. This allows us to send the capital of the activate_key.
    if event.vkCode == w.VK_LSHIFT:
        return state.toggle_shifted(event)

    if (
        event.vkCode == get_keycode(activate_key)
        and not state.shifted
        and not state.sending_replacement
    ):
        return state.toggle_layer(event)

    if state.layer_active:
        # This allows us to send the activate_key when pressing the replace_key.
        if event.action == WM_KEYDOWN and event.vkCode == get_keycode(replace_key):
            return state.send_replacement()
        else:
            return handle_layer(event, layer_binds)

    return handle_layer(event, permanent_binds)


def main() -> None:
    state = State()

    global icon
    icon = setup_icon(state)
    # Start icon in separate thread
    threading.Thread(target=icon.run).start()

    w.hook_keyboard(callback)
    w.wait_messages()


if __name__ == "__main__":
    main()
