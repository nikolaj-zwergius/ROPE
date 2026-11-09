import sys
from rope.validation import validator
from rope.utils.cli_helper import WideFormatter
from rope.io.pdb_file_cleaner import clean_rna_lib_pdb_files
import argparse

def library_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Validate PDB modules and generate/update library files",
    prog="rope-library",
    formatter_class=WideFormatter
    )


    return parser


def main() -> None:
    args = library_parser().parse_args(sys.argv[1:])
    clean_rna_lib_pdb_files()
    validator.validator()

if __name__ == "__main__":
    main()
