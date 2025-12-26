# no clue what imma do with this ngl

import os


def edit_prompt(path):
    if os.name == "nt":
        os.system(f"notepad {path}")
    elif os.name == "unix":  # TODO: test this
        os.system(f"$EDITOR {path}")

    print("Closing edito")
