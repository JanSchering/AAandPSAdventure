from enum import Enum

class STATE_KEYS(Enum):
    ROOMS = "rooms"
    PEOPLE = "people"
    CHAP = "chapter"
    CHECKP = "checkpoint"
    ITEMS = "items"
    CHR_NAME = "char_name"


class SEC_KEYS(Enum):
    TYPE = "type"
    CHECKP = "checkpoint"
    RES = "responses"
    CHOICES = "choices"
    MSG = "message"
    NAME = "name"
    ITEM = "item"
    PER = "person"
    ROOM = "room"


class RES_KEYS(Enum):
    HOOK = "hook"
    CHAP = "chapter"

class COND_KEYS(Enum):
    ATTR = "attr"
    COMPARATOR = "comp_type"
    VAL = "value"


class SEC_TYPES(Enum):
    ENDP = "endpoint"
    COND = "conditional"
    LIST = "list"
    INPUT = "input"