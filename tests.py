import os
from pathlib import Path

raw_path = "./test/test/test3"

# create directories if they don't exist
Path(raw_path).mkdir(parents=True, exist_ok=True)
