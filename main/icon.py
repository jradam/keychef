import PIL.Image
import os
import pystray
import sys
import threading


# Required for pyinstaller to find files
def absolute_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


image = PIL.Image.open(absolute_path("icon.png"))
running = True


def on_clicked(icon, item):
    if str(item) == "Settings":
        global settings
        # TODO: Open settings...
    elif str(item) == "Exit":
        global running
        running = False
        icon.stop()


icon = pystray.Icon(
    "Keychef",
    image,
    menu=pystray.Menu(
        pystray.MenuItem("Settings", on_clicked), pystray.MenuItem("Exit", on_clicked)
    ),
)

# Start icon in separate thread
threading.Thread(target=icon.run).start()
