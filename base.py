# %%
"""
list prompt example
"""
from __future__ import print_function, unicode_literals
import json
from os import path, getcwd
from whaaaaat import prompt
from util import style

question_dir = path.join(getcwd(), "questions")


cur = {}
q_file = path.join(question_dir, "prelude.json")
with open(q_file) as f:
    cur = json.load(f)
p = cur["root"]
while True:
    ans = prompt(p, style=style)
    an_idx = p["choices"].index(ans[p["name"]])
    try:
        # see if a done flag was provided in the response
        res = p["responses"][an_idx]
    except:
        print("EOG reached.")
    chapter = res["chapter"]
    hook = res["hook"]
    if chapter == "same":
        p = cur[hook]
    else:
        with open(path.join(question_dir, "{}.json".format(chapter))) as f:
            cur = json.load(f)
        p = cur[hook]
