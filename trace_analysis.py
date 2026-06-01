import sys
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



def trace_analysis_out(pattern_file, sequence_file=None,out=True,input_grid=None):
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
    repeat_map, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites = count_repeats(scrubbed_sequence)
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
        with open("trace.txt", "w", encoding="utf-8") as output:
            output.write(f"{name}\n")
            output.write(f"{structure_map}\n")
            output.write(f"{seq_output}\n\n")
            output.write("My Structure map:  \n")
            output.write(f"{structure_map} \n\n")
            output.write("2D diagram with sequence\n")
            structure_printer(output, grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir)
    else:
        return grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trace_analysis.py pattern.txt [sequence.txt]")
        sys.exit(1)
    pattern_file = sys.argv[1]
    sequence_file = sys.argv[2] if len(sys.argv) > 2 else None
    trace_analysis_out(pattern_file, sequence_file)
