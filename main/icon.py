from main.helpers import absolute_path
import PIL.Image
import pystray


def setup_icon(state) -> pystray.Icon:
    def click(icon, item):
        if str(item) == "Exit":
            icon.stop()
            state.exit()

    icon = pystray.Icon(
        "Keychef",
        PIL.Image.open(absolute_path("icon.png")),
        menu=pystray.Menu(
            pystray.MenuItem("Settings", click), pystray.MenuItem("Exit", click)
        ),
    )

    return icon
