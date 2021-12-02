from whaaaaat import style_from_dict, Token
from enum import Enum

style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


class Keys(Enum):
    CHECKP = "checkpoint"
    RES = "responses"
    CHOICES = "choices"
    HOOK = "hook"
    CHAP = "chapter"
    MSG = "message"
    NAME = "name"


init_state = {
    "chapter": "prelude",
    "checkpoint": 0,
    "items": []
}


def add_linesep(str, indicator):
    """
    adds a line separator into the string at every spot the indicator occurs.
    """
    return str.replace(indicator, "{}\n".format(indicator))
