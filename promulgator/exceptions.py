import sys
import textwrap

class PromulgatorException(Exception):
    """Base class for all exceptions. Allow extra help info to be delivered."""

    def __init__(self, message: str, help: None | str = None):
        super().__init__(message)
        self.level = "Error"
        self.help = help

    def print(self, file = sys.stderr):
        """Pretty printer for the exception."""
        output = self.level + ": "
        indent = "\n" + len(output) * " "
        output = output + indent.join(textwrap.wrap(str(self)))
        if self.help:
            output = output + "\n" + indent + indent.join(textwrap.wrap(self.help))

        print("\n", output, "\n", file=file, sep="")


class SetupError(PromulgatorException):
    """Errors during setup and before publishing"""

    pass
