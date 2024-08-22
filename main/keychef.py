from .dictionary import keys
from .helpers import get_keycode
from .icon import setup_icon
from .keychef_types import BindList
from .settings import (
    activate_key,
    exit_key,
    layer_binds,
    permanent_binds,
    replace_key,
)
from .state import State
import threading
import winput as w

# TODO: Mouse movement
# TODO: Make settings a json file
# TODO: Dictionary currently for UK layout. Can detect layout?
# TODO: First iteration of settings - just show console window
# TODO: Add option to show or hide settings/console on startup


def main() -> None:
    block: int = w.WP_DONT_PASS_INPUT_ON
    unhook: int = w.WP_UNHOOK
    stop: int = w.WP_STOP

    state = State()
    icon = setup_icon(state)

    # Start icon in separate thread
    threading.Thread(target=icon.run).start()

    def handle_layer(event: w.KeyboardEvent, binds: BindList) -> int | None:
        for bind in binds:
            if event.vkCode == get_keycode(bind["key"]):
                output_key, output_shift = keys[bind["output"]]

                if event.action == w.WM_KEYDOWN:
                    if output_shift:
                        w.press_key(w.VK_SHIFT)
                    w.press_key(output_key)

                if event.action == w.WM_KEYUP:
                    if output_shift:
                        w.release_key(w.VK_SHIFT)
                    w.release_key(output_key)

                return block
        return None

    def callback(event: w.KeyboardEvent) -> int | None:
        if not state.running:
            return unhook | stop

        if state.layer_active and event.vkCode == get_keycode(exit_key):
            icon.stop()
            state.exit()
            return block

        # Activate `shifted` when pressing shift key. This allows us to send the capital of the activate_key.
        if event.vkCode == w.VK_LSHIFT:
            state.toggle_shifted(event)
            return None

        if (
            event.vkCode == get_keycode(activate_key)
            and not state.shifted
            and not state.sending_replacement
        ):
            state.toggle_layer(event)
            return block

        if state.layer_active:
            # This allows us to send the activate_key when pressing the replace_key.
            if event.action == w.WM_KEYDOWN and event.vkCode == get_keycode(
                replace_key
            ):
                state.send_replacement()
                return block
            else:
                return handle_layer(event, layer_binds)

        return handle_layer(event, permanent_binds)

    w.hook_keyboard(callback)
    w.wait_messages()
