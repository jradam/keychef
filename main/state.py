from .helpers import hit, get_keycode
from .settings import on_activate, activate_key
import winput as w

block: int = w.WP_DONT_PASS_INPUT_ON


class State:
    def __init__(self) -> None:
        self.running: bool = True
        self.layer_active: bool = False
        self.shifted: bool = False
        self.sending_replacement: bool = False

    def exit(self) -> None:
        self.running = False
        hit(w.VK_ESCAPE)  # Hit key to trigger callback, which then quits

    def toggle_layer(self, event: w.KeyboardEvent) -> None:
        if event.action == w.WM_KEYDOWN:
            self.layer_active = True
            w.press_key(get_keycode(on_activate))
        elif event.action == w.WM_KEYUP:
            self.layer_active = False
            w.release_key(get_keycode(on_activate))

    def toggle_shifted(self, event: w.KeyboardEvent) -> None:
        if event.action == w.WM_KEYDOWN:
            self.shifted = True
        elif event.action == w.WM_KEYUP:
            self.shifted = False

    def send_replacement(self) -> None:
        self.sending_replacement = True
        hit(get_keycode(activate_key))
        self.sending_replacement = False
