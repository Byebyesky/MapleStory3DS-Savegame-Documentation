#!/usr/bin/env python3
from save_file import SaveFile


class MainQuest(SaveFile):
    parts = {"activeMainQuest": 4}
    num_bytes = sum(parts.values())

    def __init__(self, contents):
        super().__init__(contents)


if __name__ == "__main__":
    with open("../testSave/slot_1/mainQuest.dat", "rb") as f:
        contents = f.read()
        mq = MainQuest(contents)
        print("MainQuest.activeMainQuest:", mq.activeMainQuest)
