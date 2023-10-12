from .__imports import *
from .content_files import get_content_files_to_be_published

"""Publish markdown files as html documents."""


def promulgator(
    paths: Path | list[Path], verbosity: Verbosity = Verbosity.ERROR
) -> None:
    if type(paths) is not list:
        paths = [paths]

    content_files = get_content_files_to_be_published(paths)

    from pprint import pprint

    for item in content_files:
        pprint(item)

    print(f"{verbosity=}")
