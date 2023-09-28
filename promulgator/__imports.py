import sys
import os
import re
import yaml
from typing import TypeAlias

# Variable types
Path: TypeAlias = str  # May be a file or directory
DirName: TypeAlias = str
FileName: TypeAlias = str
Config: TypeAlias = dict
FileSeekingError: TypeAlias = FileNotFoundError

# Constants
ROOT_CONFIG_FILE_RE = re.compile(
    r"^\.promulgator(?:\.ya?ml)?$"
)  # Root config file must exist
METADATA_FILE_RE = re.compile(
    r"^\.metadata(?:\.ya?ml)?$"
)  # Additional config for current directory
CONTENT_FILE_RE = re.compile(
    r"\.md$"
)  # Only files that match this pattern will be published
