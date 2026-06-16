from enum import Enum


class ZoneType(Enum):
    """"Zone type for hub"""
    PRIORITY = 0
    NORMAL = 1
    RESTRICTED = 2
    BLOCKED = 3
