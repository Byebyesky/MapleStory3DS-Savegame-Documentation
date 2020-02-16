#!/usr/bin/env python3
from save_file import SaveFile


class PlayerData(SaveFile):
    parts = {
        "level": 1,
        "padding": 3,
        "experience": 4,
        "currentHp": 2,
        "currentMp": 2,
        "currentMap": 4,
        "NPCSomething": 16,
        "padding1": 48,
        "companionNPCString": 16,
        "padding2": 8,
        "LSkill": 1,
        "YSkill": 1,
        "XSkill": 1,
        "RSkill": 1,
        "UpLSkill": 1,
        "UpYSkill": 1,
        "UpXSkill": 1,
        "UpRSkill": 1,
        "learnedSkills": 2,
        "padding3": 4,
        "newIndicator": 2,
        "padding4": 4,
    }
    num_bytes = sum(parts.values())

    def __init__(self, contents):
        super().__init__(contents)
        self.property_to_byte_list("padding", 1)
        self.property_to_byte_list("NPCSomething", 1)
        self.property_to_byte_list("padding1", 1)
        self.property_to_byte_list("companionNPCString", 1)
        self.property_to_byte_list("padding2", 1)
        self.property_to_byte_list("padding3", 1)
        self.property_to_byte_list("padding4", 1)


if __name__ == "__main__":
    with open("../testSave/slot_1/playerData.dat", "rb") as f:
        contents = f.read()
        pd = PlayerData(contents)
        print("PlayerData.NPCSomething:", pd.NPCSomething)
