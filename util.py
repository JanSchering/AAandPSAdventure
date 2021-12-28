from whaaaaat import style_from_dict, Token   
from os import path, getcwd, listdir, remove
from datetime import datetime
import json
from enums import STATE_KEYS

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


init_state = {
    "chapter": "prelude",
    "checkpoint": 0,
    "items": [],
    "people": [],
    "rooms": []
}


def handle_Checkpoint(state, chap_name, cur_sec):
    print("CHECKPOINT REACHED")

    # save chapter name and checkpoint in chapter in current state
    state[STATE_KEYS.CHAP.value] = chap_name
    state[STATE_KEYS.CHECKP.value] = cur_sec[STATE_KEYS.CHECKP.value]

    # get list of current save states and sort
    saveState_files = listdir(path.join(getcwd(), "saveStates"))
    saveState_files.sort()

    # make sure only 3 save files are saved at once by deleting the oldest one if over
    if len(saveState_files) == MAX_SAVED:
        remove(path.join(state_path, saveState_files[-1]))

    # save current checkpoint state in a file named by date
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(path.join(state_path, f"{timestamp}.json"), "w") as f:
        json.dump(state, f)

    return state


def pre_process_msg(state, msg):

    # Line wrapping after the max length is reached
    max_len = 150 # TODO: Decide on a suitable length
    # Turn the message into list of characters
    l = list(msg)
    for i in range(max_len, len(msg), max_len):
        separators = [".", "?", "!", ",", " ", "-"]
        # Handle the case where the line is wrapped between two words
        if l[i] in separators or l[i+1] in separators:
            l[i] = f"{l[i]}\n"
        # Handle the case where the line is wrapped within a word
        else:
            l[i] = f"{l[i]}-\n"
    msg = "".join(l)

    # replace mentions of the character name with chosen user name
    try:
        name = state["char_name"]
        msg = msg.replace("{char_name}", name)
    except:
        pass

    return msg
