from rope.core.variant_gen_logic import variant_gen
import argparse
from rope.utils.cli_helper import WideFormatter
import sys

def variant_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Make variant blueprints from a base blueprint",
    prog="rope-variant",
    formatter_class=WideFormatter
    )

    parser.add_argument(
        "file",
        nargs="?",
        metavar="input file",
        help="Input blueprint file"
    )


    return parser

def main():
    args = variant_parser().parse_args(sys.argv[1:])
    variant_gen()

if __name__ == "__main__":
      main()