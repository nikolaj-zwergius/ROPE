import getopt,sys,os
SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

import sys
from pathlib import Path
from rope.io.structure_printers import trace_pattern_out
from rope.core.trace_logic import generate_np_pattern, trace_backbone
from rope.io.blueprint_reader import parse_header
# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main():
    try:
        opts = sys.argv
        file = os.getcwd()/Path(opts[1])
    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        header = parse_header(file)
        pattern = generate_np_pattern(file)
        seq,base_pair,_,_= trace_backbone(pattern,header=header)
        trace_pattern_out(file,seq,base_pair)
        print("done")
    except IndexError:
        print("no file given")
        raise

if __name__ == "__main__":
    main()



