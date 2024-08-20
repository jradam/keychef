# requirements.txt

```txt
pillow==10.2.0
pystray==0.19.5
winput==1.5.0

```

# readme.md

```md
<div align="center">

### KeyChef

###### a tiny keyboard layer management tool

[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)](https://www.python.org)
[![Windows](https://shields.io/badge/Windows--9cf?logo=Windows&style=social)](https://www.microsoft.com/software-download/windows11)

</div>
<br />

### Why do I exist?

If you do any programming, you might agree that brackets and symbols are used frequently, but are relatively difficult to reach on the keyboard. This small tool adds a new keyboard layer that puts these keys closer to the home row.

### Usage

Activate the new layer by holding the `activate_key` (default `;`).

Your `activate_key` key will not actually be sent, so ensure you bind this to a new key on the new layer.

KeyChef can also send a press `on_activate` (default `F13`).

### Notes

To get started with this project, install the required dependencies with `pip install -r requirements.txt`

You can build the Windows executable by running `pyinstaller --onedir --noconfirm --add-data "main/icon.png;." keychef.pyw` in a Windows environment.

```

# keychef.spec

```spec
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['keychef.pyw'],
    pathex=[],
    binaries=[],
    datas=[('main/icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='keychef',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='keychef',
)

```

# keychef.pyw

```pyw
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

```

# LICENSE

```
Copyright (c) 2024 James Adam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

# .gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/


```

# main/settings.py

```py
from winput import VK_OEM_1, VK_F13

activate_key = VK_OEM_1
on_activate = VK_F13

```

# main/icon.py

```py
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

```

# main/icon.png

This is a binary file of the type: Image

# main/helpers.py

```py
import winput as w
from winput import (
    VK_SHIFT,
    WM_KEYDOWN,
    WM_KEYUP,
)
import os
import sys


# Required for pyinstaller to find files
def absolute_path(relative_path) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def hit(key) -> None:
    w.press_key(key)
    w.release_key(key)


def shift_hit(key) -> None:
    w.press_key(VK_SHIFT)
    hit(key)
    w.release_key(VK_SHIFT)


def press(key, shift=False) -> None:
    if shift == True:
        shift_hit(key)
    else:
        hit(key)


def remap(event: w.KeyboardEvent, from_key, to_key) -> bool:
    if event.vkCode == from_key:
        if event.action == WM_KEYDOWN:
            w.press_key(to_key)
        elif event.action == WM_KEYUP:
            w.release_key(to_key)
        return True
    return False

```

# main/double.py

```py
import time
from typing import Tuple
import winput as w
from main.helpers import hit, press


DOUBLE_TAP_SPEED: float = 0.15
last_key_time: float = 0
last_key: int | None = None


def double(key1: Tuple[int, bool], key2: Tuple[int, bool]) -> None:
    global last_key_time, last_key
    current_time = time.time()
    if last_key == key1[0] and (current_time - last_key_time) < DOUBLE_TAP_SPEED:
        hit(w.VK_BACK)
        press(*key2)
    else:
        press(*key1)
    last_key_time = current_time
    last_key = key1[0]

```

