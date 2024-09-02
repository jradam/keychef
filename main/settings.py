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
    {"key": "a", "output": "ampersand"},
    {"key": "b", "output": "bracket_close"},
    # {"key": "c", "output": ""}, # In use above
    {"key": "d", "output": "parenthesis_close"},
    {"key": "e", "output": "equals"},
    {"key": "f", "output": "brace_open"},
    {"key": "g", "output": "brace_close"},
    {"key": "h", "output": "left"},
    {"key": "i", "output": "minus"},
    {"key": "j", "output": "down"},
    {"key": "k", "output": "up"},
    {"key": "l", "output": "right"},
    {"key": "m", "output": "dollar"},
    {"key": "n", "output": "return"},
    {"key": "o", "output": ""},
    {"key": "p", "output": ""},
    # {"key": "q", "output": ""}, # In use above
    {"key": "r", "output": ""},
    {"key": "s", "output": "parenthesis_open"},
    {"key": "t", "output": ""},
    {"key": "u", "output": "underscore"},
    {"key": "v", "output": "bracket_open"},
    {"key": "w", "output": "capslock"},
    {"key": "x", "output": "delete"},
    {"key": "y", "output": ""},
    {"key": "z", "output": ""},
    {"key": "space", "output": ""},
]
