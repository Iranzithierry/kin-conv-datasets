
# /*
# * Copyright (c) 2024 IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


import os
import datetime
from pathlib import Path

copyright = f"""
# /*
# * Copyright (c) {datetime.datetime.now().year} IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


"""

extensions = ['.py', '.go'] 

file_dir = Path(__file__).resolve().parent
for file in file_dir.iterdir():
    if file.is_dir():
        for subfile in file.iterdir():
            if subfile.is_file() and subfile.suffix in extensions:
                contents = subfile.open('r').read()
                contents = copyright + contents
                subfile.open('w').write(contents)

    if file.is_file() and file.suffix in extensions:
        contents = file.open('r').read()
        contents = copyright + contents
        file.open('w').write(contents)
print("Copyright header added to all .py and .go files")