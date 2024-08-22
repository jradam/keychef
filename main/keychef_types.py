from typing import Dict, Tuple, List

KeyCode = int
ShiftStatus = bool
Key = Tuple[KeyCode, ShiftStatus]
Dictionary = Dict[str, Key]
UserBind = Dict[str, str]
BindList = List[UserBind]
