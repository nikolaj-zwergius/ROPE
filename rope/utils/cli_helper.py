import argparse


class WideFormatter(argparse.RawTextHelpFormatter):
    """Preserve explicit help-text line breaks and wrap CLI help at 140 columns."""

    def __init__(self, prog: str) -> None:
        super().__init__(
            prog,
            max_help_position=40,   # column where help starts
            width=140               # total line width
        )
