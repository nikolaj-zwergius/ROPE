import sys
import os
from rope.core.analysis_logic import trace_analysis_out
import argparse
from rope.utils.cli_helper import WideFormatter

def analysis_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    prog="rope-analysis",
    description="Analysis of ROAD style blueprint",
    formatter_class=WideFormatter
    )
    parser.add_argument(
        "file",
        nargs="?",
        metavar="input file",
        help="Input file if none given all valid files in folder will be processed"
    )

    return parser


def main():
    wd = os.getcwd()
    args = analysis_parser().parse_args(sys.argv[1:])
    print(args)
    folder = f"{wd}/Trace_analysis"
    if not os.path.exists(folder):
        os.makedirs(folder)

    if args.file is None:
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                out =  f"{folder}/{file.split('.')[0]}_analysis.txt"
                trace_analysis_out(file,outfile=out)
                pass
    else:
        for file in args.file:
            file = str(file.lstrip(f".{chr(92)}"))
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split('.')[:-1]}")
                continue
            if file in os.listdir():
                trace_analysis_out(file,outfile=f"{folder}/{file.split('. ')[0]}_analysis.txt")
                pass
            else:
                print(f"{file} not found in folder")


if __name__ == "__main__":

    main()