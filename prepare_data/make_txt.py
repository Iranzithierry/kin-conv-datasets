
# /*
# * Copyright (c) 2024 IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


import json
from pathlib import Path

def extract_messages(chat_data):
    """
    Extracts the messages and sender/receiver info from the chat data
    and returns them in a dialogue format.
    """

    messages = []

    current_sender = None
    current_message = ""

    for message in chat_data:
        if message["sender"] == "Me":
            if current_sender == "BOT":
                messages.append(current_message)
                current_message = ""
            current_sender = "BOT"
        else:
            if current_sender == "USER":
                messages.append(current_message)
                current_message = ""
            current_sender = "USER"

        current_message += f"[{current_sender}] {message['message']}\n"

    # Append the last message
    messages.append(current_message)

    return ''.join(messages)

if __name__ == "__main__":
    json_path = Path("../data-[SANITIZED].json")
    output_filename = "data.txt"

    with open(json_path) as f:
        json_data = json.load(f)

    messages = extract_messages(json_data)

    with open(output_filename, "w") as f:
        f.write(messages)
