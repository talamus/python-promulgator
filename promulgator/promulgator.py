from .__imports import *
from .setup import *


def promulgator(content: Path | list[Path], verbose: bool = False) -> None:
    if type(content) is not list:
        content = [content]

    content_files = get_content_files_to_be_published(content)

    from pprint import pprint

    for item in content_files:
        pprint(item)
