from main.helpers import get_keycode

# User settings
activate_key = get_keycode("semicolon")
on_activate = get_keycode("F13")
replace_key = "c"

# Binds that are always active
permanent_binds = [
    {"key": "capslock", "output": "escape"},
]

# Binds for when the keychef layer is active
layer_binds = [
    {"key": "m", "output": "dollar"},
    {"key": "f", "output": "brace_open"},
    {"key": "j", "output": "brace_close"},
    {"key": "d", "output": "parenthesis_open"},
    {"key": "k", "output": "parenthesis_close"},
    {"key": "s", "output": "bracket_open"},
    {"key": "l", "output": "bracket_close"},
    {"key": "g", "output": "minus"},
    {"key": "u", "output": "underscore"},
    {"key": "a", "output": "ampersand"},
    {"key": "e", "output": "plus"},
    {"key": "n", "output": "return"},
    {"key": "space", "output": "backspace"},
    {"key": "x", "output": "delete"},
    {"key": "capslock", "output": "capslock"},
]
