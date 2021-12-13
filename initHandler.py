from __future__ import print_function, unicode_literals
import json
from os import path, getcwd, listdir, mkdir
from whaaaaat import prompt
from util import style, init_state, Keys, state_path


def get_init_state():
    # if does not exist, create a directory to hold the saved states
    if not path.exists(state_path):
        mkdir(state_path)

    # get and sort the pre-existing save state files
    saveState_files = listdir(path.join(getcwd(), "saveStates"))
    saveState_files.sort()

    # if saved files exist offer the user to choose a previous state
    if len(saveState_files) > 0:
        # load each existing save state
        saveStates = [json.load(open(path.join(state_path, file_path)))
                      for file_path in saveState_files]

        # extract info from saved state
        content = [str({Keys.CHAP.value: saveState[Keys.CHAP.value],
                        Keys.CHECKP.value: saveState[Keys.CHECKP.value],
                        Keys.NAME.value: saveState[Keys.CHR_NAME.value]}) for saveState in saveStates]

        # prompt user to to choose an old saved state or start new game
        prompt_name = "loadstate_prompt"
        opt_new_game = "new game"
        load_prompt = {
            "type": "list",
            "name": prompt_name,
            "message": "Choose the checkpoint to load",
            "choices": [*content, opt_new_game],
        }
        # get answer from user and fills in prompt_name with the answer
        ans = prompt(load_prompt, style=style)

        # use clean state for new games
        if ans[prompt_name] == opt_new_game:
            state = init_state
        # fill state based on choice
        else:
            # get index of chosen save state
            an_idx = load_prompt[Keys.CHOICES.value].index(ans[prompt_name])
            state = saveStates[an_idx]
    else:
        state = init_state

    return state
