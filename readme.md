<div align="center">

### KeyChef

###### a tiny keyboard layer management tool

[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)](https://www.python.org)

</div>
<br />

### Why do I exist?

If you do any programming, you might agree that brackets and symbols are used frequently, but are relatively difficult to reach on the keyboard. This small tool adds a new keyboard layer that puts these keys closer to the home row.

### Usage

Activate the new layer by holding the `activate_key` (default `;`).

Your `activate_key` key will not actually be sent, so ensure you bind this to a new key on the new layer.

KeyChef can also send a press `on_activate` (default `F13`).

### Notes

Build Windows executable by running `pyinstaller --onedir --noconfirm --add-data "icon.png;." keychef.pyw` in a Windows environment.
