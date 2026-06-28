import sys
import os
from rope.core.analysis_logic import trace_analysis_out
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))



def main():
    wd = os.getcwd()

    if len(sys.argv) < 1:
        print("Usage for specific files: batch_revolvr <file1> [<file2> ...]")
        print("Usage for all in folder: batch_revolvr")
        sys.exit(1)
    folder = f"{wd}/Trace_analysis"
    if not os.path.exists(folder):
        os.makedirs(folder)

    args = sys.argv[1:]
    if len(args) == 0:
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                trace_analysis_out(file,outfile=f"{folder}/{file.split(".")[0]}_analysis.txt")
    else:
        for file in args:
            file = str(file.lstrip(f".{chr(92)}"))
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split(".")[:-1]}")
                continue
            if file in os.listdir():
                trace_analysis_out(file,outfile=f"{folder}/{file.split(".")[0]}_analysis.txt")
            else:
                print(f"{file} not found in folder")


if __name__ == "__main__":

    main()