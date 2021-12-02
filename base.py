# %%
"""
list prompt example
"""
from __future__ import print_function, unicode_literals
import json
from os import path, getcwd, listdir, remove, mkdir
from whaaaaat import prompt
from util import style, add_linesep, init_state, Keys
from datetime import datetime

question_dir = path.join(getcwd(), "chapters")
state_path = path.join(getcwd(), "saveStates")
if not path.exists(state_path):
    mkdir(state_path)

saveState_files = listdir(path.join(getcwd(), "saveStates"))
saveState_files.sort()
timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
if len(saveState_files) > 0:
    saveStates = [json.load(open(path.join(state_path, file_path)))
                  for file_path in saveState_files]
    content = [str({Keys.CHAP.value: saveState[Keys.CHAP.value],
                    Keys.CHECKP.value: saveState[Keys.CHECKP.value]}) for saveState in saveStates]
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
            json.dump(init_state, f)
        if len(saveState_files) == 3:
            remove(saveState_files[-1])
    else:
        an_idx = load_prompt[Keys.CHOICES.value].index(ans[prompt_name])
        with open(path.join(state_path, saveState_files[an_idx]), "r") as f:
            state = json.load(f)
else:
    with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
        state = init_state
        json.dump(init_state, f)


cur_chap = {}
chap_name = state[Keys.CHAP.value]
print(chap_name)
cur_sec = {}
q_file = path.join(question_dir, "{}.json".format(chap_name))
with open(q_file) as f:
    cur_chap = json.load(f)
for sec_key in cur_chap:
    sec = cur_chap[sec_key]
    if Keys.CHECKP.value in sec.keys() and sec[Keys.CHECKP.value] == state[Keys.CHECKP.value]:
        cur_sec = sec
while True:
    # basic pre-processing to ensure that the lines don't get overly long
    cur_sec[Keys.MSG.value] = add_linesep(cur_sec[Keys.MSG.value], ".")
    ans = prompt(cur_sec, style=style)
    if not Keys.RES.value in cur_sec.keys():
        # No responses available, implies the game is over
        print("EOG reached.")
        break
    an_idx = cur_sec[Keys.CHOICES.value].index(ans[cur_sec[Keys.NAME.value]])
    res = cur_sec[Keys.RES.value][an_idx]
    # Update Current checkpoint if a new one is encountered
    if Keys.CHECKP.value in cur_sec.keys() and not(chap_name == "prelude" and cur_sec[Keys.CHECKP.value] == 0):
        print("CHECKPOINT REACHED")
        state[Keys.CHAP.value] = chap_name
        state[Keys.CHECKP.value] = cur_sec[Keys.CHECKP.value]
        saveState_files = listdir(path.join(getcwd(), "saveStates"))
        saveState_files.sort()
        print(saveState_files)
        if len(saveState_files) == 3:
            remove(path.join(state_path, saveState_files[-1]))
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        with open(path.join(state_path, "{}.json".format(timestamp)), "w") as f:
            state = init_state
            json.dump(state, f)
    chapter = res[Keys.CHAP.value]
    hook = res[Keys.HOOK.value]
    if chapter == "same":
        cur_sec = cur_chap[hook]
    else:
        chap_name = chapter
        with open(path.join(question_dir, "{}.json".format(chapter))) as f:
            cur_chap = json.load(f)
        cur_sec = cur_chap[hook]
