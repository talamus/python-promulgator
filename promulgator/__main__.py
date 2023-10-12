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
        "paths",
        metavar="content",
        nargs="+",
        help="content to be processed (directory or a markdown file)",
    )
    # argparser.add_argument(
    #     "-c",
    #     "--config",
    #     action="count",
    #     default=0,
    #     help="increase output verbosity (-v = INFO, -vv = DEBUG)",
    # )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="set output verbosity (-v = INFO, -vv = DEBUG)",
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_const",
        const=-1,
        help="Do not output anything",
    )
    argparser.epilog = """Here will be an example..."""
    return argparser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.verbose = (
        len(Verbosity) if args.verbose + 2 > len(Verbosity) else args.verbose + 2
    )
    args = {"paths": args.paths, "verbosity": Verbosity(args.verbose)}

    try:
        promulgator(**args)
    except SetupError as error:
        error.print()
        sys.exit(1)
    sys.exit(0)
