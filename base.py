from __future__ import print_function, unicode_literals
import json
from os import path
from whaaaaat import prompt
from util import handle_Checkpoint, style, Keys, question_dir, pre_process_msg
from initHandler import get_init_state

state = get_init_state()
chap_name = state[Keys.CHAP.value]

# load the relevant starting chapter data
cur_chap = {}
q_file = path.join(question_dir, "{}.json".format(chap_name))
with open(q_file) as f:
    cur_chap = json.load(f)

# find the checkpoint within the loaded chapter
cur_sec = {}
for sec_key in cur_chap:
    sec = cur_chap[sec_key]
    if Keys.CHECKP.value in sec.keys() and sec[Keys.CHECKP.value] == state[Keys.CHECKP.value]:
        cur_sec = sec

# flag so don't remake the checkpoint at starting point
first_save_loaded = True

# run the game
while True:
    # if reached end point, print last messgae then finish
    if cur_sec[Keys.TYPE.value] == Keys.ENDP.value:
        print(cur_sec[Keys.MSG.value])
        break

    # process next message to be well formatted
    cur_sec[Keys.MSG.value] = pre_process_msg(state, cur_sec[Keys.MSG.value])

    # extract the potential user response data
    responses = cur_sec[Keys.RES.value]
    # delete response data so prompt is in correct format to offer choices to user
    del cur_sec[Keys.RES.value]

    # give user choices and record the choosen response
    ans = prompt(cur_sec, style=style)
    cur_sec[Keys.RES.value] = responses # add responses back on in case need later
    ans_content = ans[cur_sec[Keys.NAME.value]]

    # save item type if needed so cannot pick up again and keeps correct format
    if Keys.ITEM.value in cur_sec.keys():
        item = cur_sec[Keys.ITEM.value]
        if item in state[Keys.ITEM.value]:
            print("You have already picked that up")
        else:
            state[Keys.ITEM.value] = item

        # to maintain format needed for prompt
        del cur_sec[Keys.ITEM.value]


    # input is only to prompt user for name
    if cur_sec[Keys.TYPE.value] == "input":
        # assign name extracted from the user response to state
        attr_name = cur_sec[Keys.NAME.value]
        state[attr_name] = ans_content

        # No choice to be made
        res = responses[0]
    # done when user only has action of picking up item available
    else:
        # the next response to print is assigned based on user choice from list
        an_idx = cur_sec[Keys.CHOICES.value].index(ans_content)
        res = responses[an_idx]


    # if section is a checkpoint as long as not very first checkpoint or a reloaded checkpoint, update state
    if Keys.CHECKP.value in cur_sec.keys() and not first_save_loaded:
        state = handle_Checkpoint(state, chap_name, cur_sec)
    elif Keys.CHECKP.value in cur_sec.keys():
        first_save_loaded = False # process the next checkpoints after the first one

    # use chosen response to find next section    
    chapter = res[Keys.CHAP.value]
    hook = res[Keys.HOOK.value]

    if chapter == "same":
        cur_sec = cur_chap[hook]
    else:
        chap_name = chapter
        with open(path.join(question_dir, "{}.json".format(chapter))) as f:
            cur_chap = json.load(f)
        cur_sec = cur_chap[hook]
