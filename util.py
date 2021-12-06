from whaaaaat import style_from_dict, Token   
from enum import Enum
from os import path, getcwd, listdir, remove
from datetime import datetime
import json

question_dir = path.join(getcwd(), "chapters")
state_path = path.join(getcwd(), "saveStates")

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
    TYPE = "type"
    CHR_NAME = "char_name"
    ENDP = "endpoint"


init_state = {
    "chapter": "prelude",
    "checkpoint": 0,
    "items": []
}


def handle_Checkpoint(state, chap_name, cur_sec):
    print("CHECKPOINT REACHED")
    state[Keys.CHAP.value] = chap_name
    state[Keys.CHECKP.value] = cur_sec[Keys.CHECKP.value]
    saveState_files = listdir(path.join(getcwd(), "saveStates"))
    saveState_files.sort()
    if len(saveState_files) == 3:
        remove(path.join(state_path, saveState_files[-1]))
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
        state = init_state
        json.dump(state, f)
    return state


def pre_process_msg(state, msg):
    try:
        msg.index("\n")
    except:
        msg = msg.replace(".", "{}\n".format("."))
    try:
        msg = msg.replace("{char_name}", "{}".format(state["char_name"]))
    except:
        pass
    return msg
