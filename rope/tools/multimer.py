
import argparse
from rope.utils.cli_helper import WideFormatter
import sys
from rope.core.grid_mapping import generate_np_pattern
from rope.utils.temp_files import cleanup_temp_files, make_temp_files
from rope.core.trace_logic import trace_backbone
from rope.io.blueprint_reader import parse_header
def multimer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Make multiple blueprints that interact with each other",
    prog="rope-multimer",
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
    args = multimer_parser().parse_args(sys.argv[1:])

    blueprints = []
    blueprint_name = []
    index = -1
    with open(args.file) as f:
        for line in f:
            if line.startswith(">"):
                blueprints.append([])
                blueprint_name.append(line.strip(">").strip())
                index += 1
            
            else:
                blueprints[index].append(line)

    temp_files = make_temp_files(blueprints, blueprint_name)
    kl_pattern = []
    patterns = []
    for temp_file in temp_files:
        pattern = generate_np_pattern(temp_file)
        patterns.append(pattern)
        kl_pattern.append(parse_header(temp_file)[1])

    print(f"Found {len(patterns)} blueprints in {args.file}.")
    print(f"Kl patterns: {kl_pattern}")

    
    cleanup_temp_files(temp_files)






if __name__ == "__main__":
      main()