import argparse
from .__imports import *
from .promulgator import promulgator

"""Command line program"""


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    argparser = argparse.ArgumentParser(
        prog="python -m promulgator",
        description="Git and Markdown Powered CMS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    argparser.add_argument(
        "content",
        metavar="content",
        nargs="+",
        help="content to be processed (directory or a markdown file)",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="be more verbose",
    )
    argparser.epilog = """Here will be an example..."""
    return argparser.parse_args()


if __name__ == "__main__":
    args = vars(parse_args())
    try:
        promulgator(**args)
    except FileSeekingError as error:
        print("Error:", error, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
