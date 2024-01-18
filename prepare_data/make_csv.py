
# /*
# * Copyright (c) 2024 IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


import json
import csv
import os
from pathlib import Path


JSON_PATH = Path("../data-[SANITIZED].json")
OUTPUT_FILENAME = "data.csv"

with open(JSON_PATH, 'r') as file:
    json_data = file.read()

chat_data = json.loads(json_data)

with open(OUTPUT_FILENAME, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Request", "Response"])

    for idx in range(0, len(chat_data), 2):
        current_message = chat_data[idx]["message"]
        next_message = chat_data[idx + 1]["message"] if idx + 1 < len(chat_data) else ""

        writer.writerow([current_message, next_message])
