import getopt,os
import sys
from pathlib import Path
from rope.io.structure_printers import trace_pattern_out
from rope.core.trace_logic import generate_np_pattern, trace_backbone
from rope.io.blueprint_reader import parse_header
from rope.utils.cli_helper import WideFormatter
import argparse

def trace_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Trace blueprint to extended dot-bracket",
    prog="rope-trace",
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
    args = trace_parser().parse_args(sys.argv[1:])
    if args.file is None:
        print("FileNotFoundError: No file given")
        exit()
    header = parse_header(args.file)
    pattern = generate_np_pattern(args.file)
    seq,base_pair,_,_= trace_backbone(pattern,header=header)
    trace_pattern_out(args.file,seq,base_pair)

if __name__ == "__main__":
    main()



