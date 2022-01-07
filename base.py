from __future__ import print_function, unicode_literals
import json
from os import path
from whaaaaat import prompt
from util import handle_Checkpoint, style, question_dir, pre_process_msg
from initHandler import get_init_state
from enums import *

ROOMS, PEOPLE, CHAP, CHECKP, ITEMS, CHR_NAME = STATE_KEYS
TYPE, CHECKP, RES, CHOICES, MSG, NAME, ITEM, PER, ROOM = SEC_KEYS
HOOK, CHAP = RES_KEYS
ATTR, COMPARATOR, VAL = COND_KEYS
ENDP, COND, LIST, INPUT = SEC_TYPES

state = get_init_state()
chap_name = state[CHAP.value]

# load the relevant starting chapter data
cur_chap = {}
q_file = path.join(question_dir, f"{chap_name}.json")
with open(q_file) as f:
    cur_chap = json.load(f)

# find the checkpoint within the loaded chapter
cur_sec = {}
for sec_key in cur_chap:
    sec = cur_chap[sec_key]
    if CHECKP.value in sec.keys() and sec[CHECKP.value] == state[CHECKP.value]:
        cur_sec = sec

# flag so don't remake the checkpoint at starting point
first_save_loaded = True

while True:
    # if reached an end point, print last message then finish
    if cur_sec[TYPE.value] == ENDP.value:
        print(cur_sec[MSG.value])
        break


    # if reached a conditional point, check condition and retrieve the valid prompt
    while cur_sec[TYPE.value] == COND.value:
        condition_info = cur_sec[COND.value]
        # Get key of the attribute to check
        attr = condition_info[ATTR.value]
        comp_type = condition_info[COMPARATOR.value]
        # Implies that we have to check for list contingency
        if comp_type == "contains":
            # stringified boolean of the conditional
            comp_res = str(condition_info[VAL.value] in state[attr])
            # replace the current section by the nested section
            cur_sec = cur_sec[comp_res]
        # Else assume that it is a direct value comparison
        else:
            # stringified boolean of the conditional
            comp_res = str(condition_info[VAL.value] == state[attr])
            # replace the current section by the nested section
            cur_sec = cur_sec[comp_res]
        

    # process next message to be well formatted, keep copy of original 
    original = cur_sec[MSG.value]
    cur_sec[MSG.value] = pre_process_msg(state, cur_sec[MSG.value])

    # extract the potential user response data
    responses = cur_sec[RES.value]
    # delete response data so prompt is in correct format to offer choices to user
    del cur_sec[RES.value]

    # give user choices and record the choosen response
    print(f"\n")
    ans = prompt(cur_sec, style=style)
    # add responses back and re-add the clean message in case need later
    cur_sec[RES.value] = responses
    cur_sec[MSG.value] = original
    # filters the content of the answer out of the object
    ans_content = ans[cur_sec[NAME.value]]

    # save item type if needed so cannot pick up again
    if ITEM.value in cur_sec.keys():
        item = cur_sec[ITEM.value]
        if item in state[ITEMS.value]:
            print("You have already picked that up")
        else:
            state[ITEMS.value].append(item)
    
    # Track special encounters
    if PER.value in cur_sec.keys():
        person = cur_sec[PER.value]
        if not person in state[PEOPLE.value]:
            state[PEOPLE.value].append(person)
    
    # Track explored special rooms 
    if ROOM.value in cur_sec.keys():
        room = cur_sec[ROOM.value]
        if not room in state[ROOMS.value]:
            state[ROOMS.value].append(person)

    # process sections that allow for user input
    if cur_sec[TYPE.value] == "input":
        # assign name extracted from the user response to state
        attr_name = cur_sec[NAME.value]
        state[attr_name] = ans_content

        # No choice to be made
        res = responses[0]
    # process 'choice' sections
    else:
        # retrieve correct response info based on index of user choice
        an_idx = cur_sec[CHOICES.value].index(ans_content)
        res = responses[an_idx]

    # if section is a checkpoint as long as not very first checkpoint or a reloaded checkpoint, update state
    if CHECKP.value in cur_sec.keys() and not first_save_loaded:
        state = handle_Checkpoint(state, chap_name, cur_sec)
    elif CHECKP.value in cur_sec.keys():
        first_save_loaded = False  # process the next checkpoints after the first one

    # use chosen response to find next section
    chapter = res[CHAP.value]
    hook = res[HOOK.value]

    if chapter == "same":
        cur_sec = cur_chap[hook]
    else:
        chap_name = chapter
        with open(path.join(question_dir, f"{chapter}.json")) as f:
            cur_chap = json.load(f)
        cur_sec = cur_chap[hook]
