import sys
import os
from utils.rope_def import (NUCLEOTIDE_CHARS,VALID_BASES,one_letter_code)
import trace_pattern as tp
from utils.trace_utils import (
    COMPLEMENT_WINDOW,
    DUPLICATE_WINDOW,
    map_structure,
    count_repeats,
    build_barriers,
    get_backbone_start,
    generate_np_pattern
)
from utils.render_utils import structure_printer
from utils.file_utils import parse_header, read_sequence_file
from trace_pattern import trace_backbone



def trace_analysis_out(pattern_file, sequence_file=None,out=True,input_grid=None,outfile=None):
    primary_sequence = None
    if out:
        name, kl_pattern = parse_header(pattern_file)
        if sequence_file:
            primary_sequence = read_sequence_file(sequence_file)

        grid = generate_np_pattern(pattern_file)
        p5,_,_= get_backbone_start(grid)
        seq, structure_map,n_map, strand_dir = tp.trace_backbone(grid)
    else:
        grid = input_grid
        p5,_,_= get_backbone_start(grid)
        seq, structure_map,n_map, strand_dir = trace_backbone(grid)
    if not p5:
        print(f"The trace through the structure failed (3p end not found). Ended at row {p5[0]}, column {p5[1]}.")
    seq_output = []
    for ch in (primary_sequence if primary_sequence is not None else seq):
        if ch == "T":
            seq_output.append("U")
        elif ch == "X":
            seq_output.append("N")
        else:
            seq_output.append(ch)
    seq_output = "".join(seq_output)

    p5, _, _ = get_backbone_start(grid)
    scrubbed_sequence, structure_map,n_map, strand_dir = tp.trace_backbone(grid)
    map_array = map_structure(structure_map)
    repeat_map, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites = count_repeats(scrubbed_sequence,bpmap=map_array)
    barriers = build_barriers(structure_map, map_array, len(scrubbed_sequence))
    wobbles_seq = ["·"] * len(scrubbed_sequence)
    for i in range(len(scrubbed_sequence)):
        partner = map_array[i] if i < len(map_array) else i
        if partner < 0 or partner >= len(scrubbed_sequence):
            continue
        left = scrubbed_sequence[i]
        right = scrubbed_sequence[partner]
        if (left == "G" and right == "U") or (left == "U" and right == "G") or (left == "K" and right == "K"):
            wobbles_seq[i] = left
            wobbles_seq[partner] = right
    if out :
        with open(f"{outfile}", "w", encoding="utf-8") as output:
            output.write(f"{name}\n")
            output.write(f"{structure_map}\n")
            output.write(f"{seq_output}\n\n")
            output.write("My Structure map:  \n")
            output.write(f"{structure_map} \n\n")
            structure_printer(output, grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir)
    else:
        return grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir

if __name__ == "__main__":

    dir_path = os.path.dirname(os.path.realpath(__file__))  
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
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
            file = str(file.split(chr(92))[1])
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split(".")[:-1]}")
                continue
            if file in os.listdir():
                trace_analysis_out(file,outfile=f"{folder}/{file.split(".")[0]}_analysis.txt")
            else:
                print(f"{file} not found in folder")
