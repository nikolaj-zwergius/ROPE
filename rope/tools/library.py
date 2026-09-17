import sys
from rope.validation import validator
from rope.utils.cli_helper import WideFormatter
import argparse

def library_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Validate PDB modules and generate/update library files",
    prog="rope-library",
    formatter_class=WideFormatter
    )


    return parser


def main():
    args = library_parser().parse_args(sys.argv[1:])
    validator.validator()

if __name__ == "__main__":
    main()
