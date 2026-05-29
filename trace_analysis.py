﻿#!/usr/bin/env python

import random
import sys
import numpy as np
import utils.rope_def as rd
import trace_pattern as tp
from utils.trace_utils import (
    COMPLEMENT_WINDOW,
    DUPLICATE_WINDOW,
    NUCLEOTIDE_CHARS,
    get_pattern_char,
    map_structure,
    count_repeats,
    build_barriers,
    render_structure_cell,
    render_strand_cell,
    render_highlight_cell,
    render_wobble_cell,
    render_barrier_cell,
    VALID_BASES,
    structure_printer
)


def read_file(path):
    with open(path, encoding="utf-8") as handle:
        content = handle.read()
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return content.split("\n")


def read_sequence_file(path):
    lines = read_file(path)
    return "".join(line.strip() for line in lines).upper()


def parse_header(file_path):
    name = "Untitled"
    kl_pattern = ""
    with open(file_path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(">"):
                name = line[1:33].strip()
            elif line.startswith("@"):
                kl_pattern = line[1:33].strip()
    return name, kl_pattern


def trace_backbone(grid, primary_sequence=None):
    p5 = rd.find_5_prime(grid)
    up, down, left, rigth = rd.check_round(grid, p5)
    if up.isalpha():
        first = (p5[0] - 1, p5[1])
        direction = rd.dir_up()
    elif down.isalpha():
        first = (p5[0] + 1, p5[1])
        direction = rd.dir_down()
    elif left.isalpha():
        first = (p5[0], p5[1] - 1)
        direction = rd.dir_left()
    elif rigth.isalpha():
        first = (p5[0], p5[1] + 1)
        direction = rd.dir_rigth()
    else:
        raise ValueError("No valid first base")

    seq = []
    n_map = {}
    strand_dir = {}
    num = 0
    next_base = first
    test_success = False
    max_steps = grid.shape[0] * grid.shape[1] * 3

    for _ in range(max_steps):
        r, c = next_base
        if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
            break

        next_base_name = get_pattern_char(grid, r, c)
        if next_base_name == "3":
            test_success = True
            break

        if next_base_name.isalpha() and next_base_name not in rd.one_letter_code.keys():
            if next_base_name == "T":
                next_base_name = "U"
            else:
                next_base_name = "N"

        if next_base_name in rd.one_letter_code.keys():
            if primary_sequence is not None:
                if num < len(primary_sequence):
                    grid[r, c] = primary_sequence[num]
                else:
                    grid[r, c] = "N"
            num += 1
            n_map[(r, c)] = num
            seq.append(str(grid[r, c]))

        strand_dir[(r, c)] = direction

        if next_base_name in direction.move_list.keys():
            direction = direction.move_list[next_base_name]()

        next_base = direction.move(next_base)

    return seq, n_map, strand_dir, test_success, p5, direction


def trace_analysis_out(pattern_file, sequence_file=None,out=True,input_grid=None):
    primary_sequence = None
    if out:
        name, kl_pattern = parse_header(pattern_file)
        if sequence_file:
            primary_sequence = read_sequence_file(sequence_file)

        grid = rd.generate_np_pattern(pattern_file)
        seq, n_map, strand_dir, success, p5, start_direction = trace_backbone(grid, primary_sequence)
    else:
        grid = input_grid
        seq, n_map, strand_dir, success, p5, start_direction = trace_backbone(grid)
    if not success:
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

    _, structure_map = tp.trace_backbone(grid)
    map_array, scrubbed_sequence = map_structure(structure_map, seq_output)
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
