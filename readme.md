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

Edit `settings.py` to configure KeyChef to your liking. Any keys you want to bind (or send) will need to be added to `dictionary.py`.

Activate the new layer by holding `activate_key` (default `;`).

Your `activate_key` key will not actually be sent, so ensure you bind this to a new key on the new layer with `replace_key`.

KeyChef can also send a press `on_activate` (default `F13`).

### Notes

To get started with this project, install the required dependencies with `pip install -r requirements.txt`

To run the app, just run `keychef.pyw`.

You can use mypy to check types by installing mypy (`pip install mypy`) and running `mypy .`

You can build a Windows executable by running `pyinstaller --onedir --noconfirm --add-data "main/icon.png;." keychef.pyw` in a Windows environment.
