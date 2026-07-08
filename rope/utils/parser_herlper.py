import argparse

class WideFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(
            prog,
            max_help_position=40,   # column where help starts
            width=140               # total line width
        )