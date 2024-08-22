from .helpers import absolute_path
from .state import State
import PIL.Image
import pystray


def setup_icon(state: State) -> pystray.Icon:
    def exit() -> None:
        icon.stop()
        state.exit()

    icon = pystray.Icon(
        "Keychef",
        PIL.Image.open(absolute_path("icon.png")),
        menu=pystray.Menu(
            pystray.MenuItem("Settings", lambda: print("Settings clicked")),
            pystray.MenuItem("Exit", lambda: exit()),
        ),
    )

    return icon
