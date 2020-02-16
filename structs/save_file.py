#!/usr/bin/env python3
import logging

logger = logging.getLogger()


class SaveFile:
    def __init__(self, contents):
        self.contents: bytes = contents
        self.parse_file()

    def parse_file(self):
        """Sets the properties for the SaveFile to the binary string value."""
        current_index = 0

        # loop through the self.parts dictionary and assign each property with the corresponding value
        for k, v in self.parts.items():
            if isinstance(v, int):
                setattr(self, k, self.contents[current_index : current_index + v])
                current_index += v
            elif v == "ItemList":
                item_list, total_bytes = self.parse_item_list(
                    self.contents[current_index:]
                )
                setattr(self, k, item_list)
                current_index += total_bytes

        self.validate_byte_length()

    def property_to_byte_list(self, property_name: str, chunk_size: int):
        """Splits a given property's byte string to a list of byte strings of size chunk_size."""
        byte_str = getattr(self, property_name, b"")
        value = [
            byte_str[i : i + chunk_size] for i in range(0, len(byte_str), chunk_size)
        ]
        setattr(self, property_name, value)

    def validate_byte_length(self):
        """Validate that the number of bytes used by the class's properties is equivalent to the number
        of bytes in contents."""
        class_len = self.num_bytes
        contents_len = len(self.contents)
        if class_len != contents_len:
            logger.warning(
                f"The length of the file contents does not match with {type(self)}"
            )
            logger.warning(f"Expected {class_len} bytes. Given {contents_len} bytes.")
