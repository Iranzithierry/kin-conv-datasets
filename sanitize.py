import json
import ftfy
import re

"""
Purpose:
This file is used to remove the non-ascii characters from the json file.
"""

OUTPUT_FILENAME = "data-[SANITIZED].json"
NEW_MESSAGES = []
NOISE = [
    "Liked a message",
    "sent an attachment",
    "You sent an attachment.",
    "liked a message" "shared a story",
    "changed the theme",
    "can now message and call",
    "missed a",
    "wasn't notified about this message",
    "You are now connected on Messenger",
    "missed your call",
    "You started a video chat",
    "You started an audio call",
    "Audio call ended",
    "Video chat ended",
    "You set the quick reaction to",
]

def decode(text_bytes: str):
    """
    Decodes raw bytes to a string.

    Args:
        text_bytes: The raw bytes to decode.

    Returns:
        The decoded string.
    """
    return ftfy.ftfy("{}".format(text_bytes))

def remove_noise(message):
    for noise in NOISE:
        message = re.sub(
                rf"\b{re.escape(noise)}\b", "", message, flags=re.IGNORECASE
        )
    return message.strip()


with open("data.json", "r") as file:
    json_data = file.read()

chat_data = json.loads(json_data)
for chat in chat_data:
    new = {
        "sender": decode(chat["sender"]),
        "receiver": decode(chat["receiver"]),
        "message": remove_noise(decode(chat["message"])),
    }
    NEW_MESSAGES.append(new)

with open(OUTPUT_FILENAME, "a") as file:
    json.dump(NEW_MESSAGES, file, indent=4)
