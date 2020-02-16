#!/usr/bin/env python3
from save_file import SaveFile
from typing import List


class Item(SaveFile):
    parts = {"id": 4, "amount": 4, "isNew": 4}
    num_bytes = sum(parts.values())

    def __init__(self, contents):
        super().__init__(contents)


class ItemList(SaveFile):
    parts = {"sizeOfVector": 4}
    empty_list_num_bytes = sum(parts.values())

    def __init__(self, contents):
        self.items: List[Item] = []
        super().__init__(contents)

    @property
    def num_bytes(self):
        num_bytes = 0
        for k, v in self.parts.items():
            num_bytes += v

        num_bytes += len(self.items) * Item.num_bytes
        return num_bytes


class Inventory(SaveFile):
    parts = {
        "quickSlot1": 4,
        "quickSlot2": 4,
        "money": 4,
        "armor": "ItemList",
        "accessory": "ItemList",
        "weapon": "ItemList",
        "shoes": "ItemList",
        "rings": "ItemList",
        "earrings": "ItemList",
        "medals": "ItemList",
        "consumables": "ItemList",
    }

    def __init__(self, contents):
        super().__init__(contents)

    def parse_item_list(self, contents):
        item_list = ItemList(contents[: ItemList.empty_list_num_bytes])
        num_items = int(
            int.from_bytes(
                item_list.sizeOfVector, byteorder="little", signed=True
            )
            / Item.num_bytes
        )
        current_index = ItemList.empty_list_num_bytes
        items = []
        for i in range(num_items):
            items.append(Item(contents[current_index : current_index + Item.num_bytes]))
            current_index += Item.num_bytes
        item_list.items = items
        return item_list, current_index

    @property
    def num_bytes(self):
        num_bytes = 0
        for k, v in self.parts.items():
            if isinstance(v, int):
                num_bytes += v
            elif v == "ItemList":
                num_bytes += getattr(self, k).num_bytes  # self.k.num_bytes
        return num_bytes


if __name__ == "__main__":
    with open("../testSave/slot_1/inventory.dat", "rb") as f:
        contents = f.read()
        inv = Inventory(contents)
        print(dir(inv))
        print("Inventory.quickSlot1:", inv.quickSlot1)
        print("Inventory.armor:", inv.armor)
        print(type(inv.armor))
        print(inv.armor.items)
        print(inv.armor.items[0].id)
        print(inv.armor.items[0].amount)
        print(inv.armor.items[0].isNew)

        print(int.from_bytes(inv.armor.items[0].id, byteorder="little", signed=False))
        print(int.from_bytes(b"\xa4\x42\x0f\x00", byteorder="little", signed=False))
