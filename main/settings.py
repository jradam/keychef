from .keychef_types import BindList

# User settings
activate_key = "semicolon"
on_activate = "F13"
replace_key = "c"
exit_key = "q"

# Binds that are always active
permanent_binds: BindList = [
    {"key": "capslock", "output": "escape"},
]

# Binds for when the KeyChef layer is active
layer_binds: BindList = [
    {"key": "i", "output": "minus"},
    {"key": "a", "output": "ampersand"},
    {"key": "d", "output": "parenthesis_close"},
    {"key": "capslock", "output": "capslock"},
    {"key": "b", "output": "bracket_close"},
    {"key": "s", "output": "parenthesis_open"},
    {"key": "e", "output": "equals"},
    {"key": "f", "output": "brace_open"},
    {"key": "g", "output": "brace_close"},
    {"key": "h", "output": "left"},
    {"key": "j", "output": "down"},
    {"key": "k", "output": "up"},
    {"key": "l", "output": "right"},
    {"key": "m", "output": "dollar"},
    {"key": "n", "output": "return"},
    {"key": "v", "output": "bracket_open"},
    {"key": "space", "output": "backspace"},
    {"key": "u", "output": "underscore"},
    {"key": "x", "output": "delete"},
]
