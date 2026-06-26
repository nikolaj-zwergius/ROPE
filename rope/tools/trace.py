import getopt,sys,os
SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

import sys
from pathlib import Path
from rope.io.structure_printers import trace_pattern_out
from rope.core.trace_logic import generate_np_pattern, trace_backbone

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main():
    try:
        opts = sys.argv

    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        pattern = generate_np_pattern(opts[1])
        seq,base_pair,_,_= trace_backbone(pattern)
        trace_pattern_out(opts[1],seq,base_pair)
        print("done")
    except IndexError:
        print("no file given")

if __name__ == "__main__":
    main()



