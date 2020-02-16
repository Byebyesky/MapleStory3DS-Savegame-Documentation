#!/usr/bin/env python3
from save_file import SaveFile


class Summary(SaveFile):
    parts = {
        "name": 18,
        "unk": 2,
        "year": 2,
        "month": 1,
        "day": 1,
        "hour": 1,
        "minute": 1,
        "chapter": 1,
        "level": 1,
        "null": 4,
        "robeEquipped": 4,
        "hatEquipped": 4,
        "weaponEquipped": 4,
        "bootsEquipped": 4,
        "ringEquipped": 4,
        "earringsEquipped": 4,
        "medalEquipped": 4,
        "playtime": 4,
    }
    num_bytes = sum(parts.values())

    def __init__(self, contents):
        super().__init__(contents)
        self.property_to_byte_list("name", 2)


if __name__ == "__main__":
    with open("../testSave/slot_1/summary_1.dat", "rb") as f:
        contents = f.read()
        s = Summary(contents)
        print("Summary.name:", s.name)
        print(type(s.contents))
