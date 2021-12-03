from __future__ import print_function, unicode_literals
import json
from os import path
from whaaaaat import prompt
from util import handle_Checkpoint, style, init_state, Keys, question_dir, state_path, pre_process_msg
from initHandler import get_init_state

state = get_init_state()

cur_chap = {}
chap_name = state[Keys.CHAP.value]
cur_sec = {}
q_file = path.join(question_dir, "{}.json".format(chap_name))
with open(q_file) as f:
    cur_chap = json.load(f)
for sec_key in cur_chap:
    sec = cur_chap[sec_key]
    if Keys.CHECKP.value in sec.keys() and sec[Keys.CHECKP.value] == state[Keys.CHECKP.value]:
        cur_sec = sec
while True:
    cur_sec[Keys.MSG.value] = pre_process_msg(state, cur_sec[Keys.MSG.value])
    if cur_sec[Keys.TYPE.value] == Keys.ENDP.value:
        print(cur_sec[Keys.MSG.value])
        break
    responses = cur_sec[Keys.RES.value]
    del cur_sec[Keys.RES.value]
    ans = prompt(cur_sec, style=style)
    ans_content = ans[cur_sec[Keys.NAME.value]]
    if cur_sec[Keys.TYPE.value] == "input":
        attr_name = cur_sec[Keys.NAME.value]
        state[attr_name] = ans_content
        # No choice to be made
        res = responses[0]
    else:
        an_idx = cur_sec[Keys.CHOICES.value].index(ans_content)
        res = responses[an_idx]
    if Keys.CHECKP.value in cur_sec.keys() and not(chap_name == "prelude" and cur_sec[Keys.CHECKP.value] == 0):
        state = handle_Checkpoint(state, chap_name, cur_sec)
    chapter = res[Keys.CHAP.value]
    hook = res[Keys.HOOK.value]
    if chapter == "same":
        cur_sec = cur_chap[hook]
    else:
        chap_name = chapter
        with open(path.join(question_dir, "{}.json".format(chapter))) as f:
            cur_chap = json.load(f)
        cur_sec = cur_chap[hook]
