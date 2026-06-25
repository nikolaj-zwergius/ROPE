
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import getopt
import sys
import numpy as np
import src.definitions.rope_def as rd
from src.io.structure_printers import flip_pattern
        

if __name__ == "__main__":
    try:
        opts = sys.argv

    except getopt.GetoptError:
            print("help_mes")
            sys.exit()
    try:
        flip_pattern(opts[1])
    except IndexError:
        print("no file given")


