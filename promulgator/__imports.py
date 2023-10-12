# fmt: off
import os
import re
import yaml
from typing import TypeAlias
from enum import Enum
from .exceptions import *

### Output verbosity

Verbosity = Enum("Verbosity", ["QUIET", "ERROR", "INFO", "DEBUG"])

### Variable types

Path:      TypeAlias = str  # May be a file or a directory
DirName:   TypeAlias = str
FileName:  TypeAlias = str
Config:    TypeAlias = dict

### File patterns

# Root config file that must exist
ROOT_CONFIG_FILE_RE = re.compile(r"^\.promulgator(?:\.ya?ml)?$")

# Additional config for current directory
METADATA_FILE_RE    = re.compile(r"^\.metadata(?:\.ya?ml)?$")

# Only files that match this pattern will be published
CONTENT_FILE_RE     = re.compile(r"\.md$")
