from __future__ import print_function, unicode_literals
import json
from os import path, getcwd, listdir, remove, mkdir
from whaaaaat import prompt
from util import style, init_state, Keys, state_path
from datetime import datetime


def get_init_state():
    if not path.exists(state_path):
        mkdir(state_path)

    saveState_files = listdir(path.join(getcwd(), "saveStates"))
    saveState_files.sort()
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    if len(saveState_files) > 0:
        saveStates = [json.load(open(path.join(state_path, file_path)))
                      for file_path in saveState_files]
        content = [str({Keys.CHAP.value: saveState[Keys.CHAP.value],
                        Keys.CHECKP.value: saveState[Keys.CHECKP.value],
                        Keys.NAME.value: saveState[Keys.CHR_NAME.value]}) for saveState in saveStates]
        prompt_name = "loadstate_prompt"
        opt_new_game = "new game"
        load_prompt = {
            "type": "list",
            "name": prompt_name,
            "message": "Choose the checkpoint to load",
            "choices": [*content, opt_new_game],
        }
        ans = prompt(load_prompt, style=style)
        if ans[prompt_name] == opt_new_game:
            with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
                state = init_state
        else:
            an_idx = load_prompt[Keys.CHOICES.value].index(ans[prompt_name])
            with open(path.join(state_path, saveState_files[an_idx]), "r") as f:
                state = json.load(f)
    else:
        with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
            state = init_state
            json.dump(init_state, f)

    return state
