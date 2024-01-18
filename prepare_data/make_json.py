# /*
# * Copyright (c) 2024 IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


import os
import json
from datetime import datetime
from pathlib import Path
import re
import asyncio
import ftfy

INBOX_DIR = Path("../data_classified/inbox/")


"""
REQUESTER_ATTR and RESPONDER_ATTR are variables that store the keys 
used in the message dictionary to identify the sender and receiver 
of each message.

REQUESTER_ATTR contains the key for the sender.
RESPONDER_ATTR contains the key for the receiver.

This allows the code to flexibly refer to the sender and receiver 
attributes in the message dictionaries.

The default values for these variables are "sender" and "receiver",
you can choose either "bot" and "user" as the sender and receiver attributes.
"""
REQUESTER_ATTR = "sender"
RESPONDER_ATTR = "receiver"


OUTPUT_FILENAME = "data-[IG].json"


"""
if the message sent by the same previous user
we will add a separator to that message inline
@example:
    {
        "sender": "user1",
        "receiver": "Me",
        "message": "Hi"
    },
    {
        "sender": "user1",
        "receiver": "Me",
        "message": "Hi again"
    }

we will add the separator then return this type of message:
    {
        "sender": "user1",
        "receiver": "Me",
        "message": "Hi<SEPARATOR> Hi again"
    }

ALLOWED_SEPARATORS = ["," "." "\n"]
"""
SEPARATOR = ","


"""
SENSITIVE_DATA is a list of strings containing sensitive information that should be redacted. 
It contains message text snippets and actions related to a Facebook messenger conversation.
"""
SENSITIVE_DATA = [
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
ALL_MESSAGES = []
NEW_MESSAGES = []

class MakeJson:
    def __init__(self, inbox_dir: Path):
        """
        Initializes the MakeJson class with the inbox directory path.
        """
        self.inbox_dir = inbox_dir
        self.inboxes_dir = os.listdir(inbox_dir)

    def decode(self, text_bytes: str):
        """Decodes raw bytes to a string.

        Args:
          text_bytes: The raw bytes to decode.

        Returns:
          The decoded string.
        """
        return ftfy.ftfy("{}".format(text_bytes))

    def get_sender(self, message):
        """
        Gets the sender name from a Facebook message.

        The sender name is extracted from the "sender_name" field of the message.
        If it is missing, "Unknown" is returned.

        The raw bytes are decoded to a string, and some name replacements are done,
        mapping specific names to "Me".

        Args:
            message: The Facebook message object.

        Returns:
            The decoded sender name, with name replacements applied.
        """
        sender = message.get("sender_name", "Unknown")
        sender = self.decode(sender)
        names = ["Thierry Bronx", "T.Roy"]
        for name in names:
            sender.replace(name, "Me")
        return sender

    def get_receiver(self, message, sender, participants):
        """
        Gets the receiver name from a Facebook message.

        Determines the receiver by checking the sender against the list of
        participants. If the sender matches the first participant, the receiver is
        the second participant, and vice versa.

        The raw bytes of the receiver name are decoded to a string, and some name
        replacements are done, mapping specific names to "Me".

        Args:
            message: The Facebook message object.
            sender: The decoded sender name.
            participants: List of participant names.

        Returns:
            The decoded receiver name, with name replacements applied.
        """
        receiver = participants[0] if sender == participants[1] else participants[1]
        receiver = self.decode(receiver)
        names = ["Thierry Bronx", "T.Roy"]
        for name in names:
            receiver.replace(name, "Me")
        return receiver

    def get_message(self, message: str, sender=""):
        """
        Cleans the message text by removing sensitive data,
        the sender name, and extra whitespace before returning the cleaned message.

        Args:
            message: The original message text.
            sender: The sender name to remove from the message.

        Returns:
            The cleaned message text with sensitive data, sender name,
            and extra whitespace removed.
        """
        for sensitive_message in SENSITIVE_DATA:
            message = re.sub(
                rf"\b{re.escape(sensitive_message)}\b", "", message, flags=re.IGNORECASE
            )

        message = message.replace(sender, "")
        message = (
            message.strip().replace(" .", ".").replace("  ", "").replace(" , ", "")
        )
        return self.decode(message)

    async def extract_data_from_json(self, file_path: Path):
        """
        Extracts message data from a Facebook message JSON file.

        Opens the given JSON file path, loads the data, extracts the participant
        names, iterates through the messages to build a list of formatted message
        objects with sender, receiver, content, and timestamp, sorts the messages
        by timestamp, and appends each message to the ALL_MESSAGES global variable.

        Returns the updated ALL_MESSAGES list containing all extracted messages.
        """
        with open(file_path, "r") as file:
            data = json.load(file)
            participants = [participant["name"] for participant in data["participants"]]

            que_messages = []
            previous_message = None

            for message in data["messages"]:
                if len(participants) > 1:
                    sender = self.get_sender(message)
                    receiver = self.get_receiver(message, sender, participants)
                    content = (
                        message.get("content", "None")
                        if "content" in message
                        else "None"
                    )
                    timestamp_ms = message.get("timestamp_ms", 0)
                    timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000.0)
                    timestamp_ms = timestamp_ms.strftime("%Y-%m-%d %H:%M:%S")

                    if previous_message and previous_message["sender"] == sender:
                        previous_message[
                            "message"
                        ] = f"{self.get_message(content, sender=sender)} {SEPARATOR} {self.get_message(previous_message['message'], sender=sender)}"
                    else:
                        previous_message = {
                            "sender": sender,
                            "receiver": receiver,
                            "message": self.get_message(content, sender=sender),
                            "timestamp_ms": timestamp_ms,
                        }
                        que_messages.append(previous_message)

            messages = sorted(
                que_messages, key=lambda x: x["timestamp_ms"], reverse=False
            )
            for message in messages:
                ALL_MESSAGES.append(message)
            return ALL_MESSAGES

    def main(self):
        """
        Iterates through each inbox directory, extracts message data from the
        message_1.json file, appends the extracted messages to the global ALL_MESSAGES
        list. Finally writes the aggregated message data to a json file.
        """
        for dir_name in self.inboxes_dir:
            dir_path = os.path.join(self.inbox_dir, dir_name)
            inbox_json_path = Path(os.path.join(dir_path, "message_1.json"))
            if os.path.exists(inbox_json_path):
                asyncio.run(self.extract_data_from_json(inbox_json_path))

        with open(OUTPUT_FILENAME, "w") as outfile:
            json.dump(ALL_MESSAGES, outfile, indent=4)


if __name__ == "__main__":
    NOW = datetime.now().strftime("%H:%M:%S")
    make_json = MakeJson(
        INBOX_DIR,
    )
    make_json.main()
