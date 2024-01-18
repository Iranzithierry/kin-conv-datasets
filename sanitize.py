import json
import ftfy

"""
Purpose:
This file is used to remove the non-ascii characters from the json file.
"""

OUTPUT_FILENAME = "data-[SANITIZED].json"
NEW_MESSAGES = []

def decode(text_bytes: str):
    """
    Decodes raw bytes to a string.

    Args:
        text_bytes: The raw bytes to decode.

    Returns:
        The decoded string.
    """
    return ftfy.ftfy("{}".format(text_bytes))


with open("data.json", "r") as file:
    json_data = file.read()

chat_data = json.loads(json_data)
for chat in chat_data:
    new = {
        "sender": decode(chat["sender"]),
        "receiver": decode(chat["receiver"]),
        "message": decode(chat["message"]),
    }
    NEW_MESSAGES.append(new)

with open(OUTPUT_FILENAME, "a") as file:
    json.dump(NEW_MESSAGES, file, indent=4)
