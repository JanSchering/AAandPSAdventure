from whaaaaat import style_from_dict, Token   
from enum import Enum
from os import path, getcwd, listdir, remove
from datetime import datetime
import json

MAX_SAVED = 3

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

    # save chapter name and checkpoint in chapter in current state
    state[Keys.CHAP.value] = chap_name
    state[Keys.CHECKP.value] = cur_sec[Keys.CHECKP.value]

    # get list of current save states and sort
    saveState_files = listdir(path.join(getcwd(), "saveStates"))
    saveState_files.sort()

    # make sure only 3 save files are saved at once by deleting the oldest one if over
    if len(saveState_files) == MAX_SAVED:
        remove(path.join(state_path, saveState_files[-1]))

    # save current checkpoint state in a file named by date
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
        json.dump(state, f)

    return state


def pre_process_msg(state, msg):
    # every sentence is a new line
    try:
        msg = msg.replace(".", "{}\n".format("."))
    except:
        pass

    # replace mentions of the character name with chosen user name
    try:
        msg = msg.replace("{char_name}", "{}".format(state["char_name"]))
    except:
        pass

    return msg
