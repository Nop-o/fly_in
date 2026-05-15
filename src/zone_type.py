from enum import Enum


class ZoneType(Enum):
    PRIORITY = 0
    NORMAL = 1
    RESTRICTED = 2
    BLOCKED = 3
