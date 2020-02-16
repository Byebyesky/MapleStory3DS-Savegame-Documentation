#!/usr/bin/env python3
from save_file import SaveFile


class Common(SaveFile):
    parts = {
        "lastSave": 2,
        "unlockedMovies": 2,
        "firstSlotUsed": 1,
        "secondSlotUsed": 1,
        "firstSlotComplete": 1,
        "secondSlotComplete": 1,
        "creditsPicture": 1,
        "unk1": 1,
        "unk2": 2,
        "padding": 36,
    }
    num_bytes = sum(parts.values())

    def __init__(self, contents):
        super().__init__(contents)
        self.property_to_byte_list("padding", 1)


if __name__ == "__main__":
    with open("../testSave/common.dat", "rb") as f:
        contents = f.read()
        c = Common(contents)
        print("Common.lastSave:", c.lastSave)
