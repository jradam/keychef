from main.helpers import absolute_path
import PIL.Image
import pystray


def setup_icon(state) -> pystray.Icon:
    icon = pystray.Icon(
        "Keychef",
        PIL.Image.open(absolute_path("icon.png")),
        menu=pystray.Menu(
            pystray.MenuItem("Settings", lambda: print("Settings clicked")),
            pystray.MenuItem("Exit", lambda: (icon.stop(), state.exit())),
        ),
    )

    return icon
