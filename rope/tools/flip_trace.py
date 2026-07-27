
import sys
from rope.io.structure_printers import flip_pattern
from rope.utils.cli_helper import WideFormatter
import argparse

def flip_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Flip blueprint",
    prog="rope-flip",
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
    args = flip_parser().parse_args(sys.argv[1:])
    if args.file is None:
        print("FileNotFoundError: ","no file given")
        exit()
    
    flip_pattern(args.file)

        
if __name__ == "__main__":
    main()


