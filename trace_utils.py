import random
import rope_def as rd

COMPLEMENT_WINDOW = 10
DUPLICATE_WINDOW = 10
KL_DELAY = 150

NUCLEOTIDE_CHARS = set("NGACURYKMSWVHBDT")
VALID_BASES = set("AUCG")


def get_backbone_start(pattern):
    p5 = rd.find_5_prime(pattern)
    up, down, left, rigth = rd.check_round(pattern, p5)
    if up.isalpha():
        return p5, (p5[0] - 1, p5[1]), rd.dir_up()
    if down.isalpha():
        return p5, (p5[0] + 1, p5[1]), rd.dir_down()
    if left.isalpha():
        return p5, (p5[0], p5[1] - 1), rd.dir_left()
    if rigth.isalpha():
        return p5, (p5[0], p5[1] + 1), rd.dir_rigth()
    raise ValueError("No valid first base")


def normalize_base_name(base_name):
    if base_name.isalpha() and base_name not in rd.one_letter_code.keys():
        return "U" if base_name == "T" else "N"
    return base_name


def get_pattern_char(grid, r, c):
    if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
        return ""
    return str(grid[r, c])


def map_structure(structure_map, sequence):
    mapping = [-1] * len(structure_map)
    stack_paren = []
    stack_brace = []
    stack_square = []

    for idx, ch in enumerate(structure_map):
        if ch == ".":
            mapping[idx] = idx
        elif ch == "(":
            stack_paren.append(idx)
        elif ch == ")":
            partner = stack_paren.pop() if stack_paren else idx
            mapping[idx] = partner
            mapping[partner] = idx
        elif ch == "[":
            stack_square.append(idx)
        elif ch == "]":
            partner = stack_square.pop() if stack_square else idx
            mapping[idx] = partner
            mapping[partner] = idx
        elif ch == "{":
            stack_brace.append(idx)
        elif ch == "}":
            partner = stack_brace.pop() if stack_brace else idx
            mapping[idx] = partner
            mapping[partner] = idx
        else:
            mapping[idx] = idx

    sequence = list(sequence)
    for idx, ch in enumerate(sequence):
        if ch not in VALID_BASES:
            partner = mapping[idx] if 0 <= idx < len(mapping) else idx
            if partner < 0 or partner >= len(sequence):
                partner = idx
            choice = random.choice(["A", "U", "G", "C"])
            complement = {"A": "U", "U": "A", "G": "C", "C": "G"}[choice]
            sequence[idx] = choice
            if 0 <= partner < len(sequence):
                sequence[partner] = complement
    return mapping, "".join(sequence)


def count_repeats(sequence, complement_window=COMPLEMENT_WINDOW, duplicate_window=DUPLICATE_WINDOW):
    strand_length = len(sequence)
    repeat_map = ["-"] * strand_length
    pattern_repeats = 0
    poly_repeats = 0
    restriction_sites = 0

    for i in range(strand_length - complement_window + 1):
        block = sequence[i : i + complement_window]
        antisense = "".join(
            rd.base_pairs_table[base]
            for base in reversed(block)
        )
        j = sequence.find(antisense, i)
        while j != -1:
            for k in range(complement_window):
                repeat_map[i + k] = "P"
                repeat_map[j + k] = "P"
            j = sequence.find(antisense, j + 1)

    complement_zones = sum(1 for value in repeat_map if value == "P")

    for i in range(strand_length - duplicate_window + 1):
        block = sequence[i : i + duplicate_window]
        j = sequence.find(block, i + 1)
        while j != -1:
            for k in range(duplicate_window):
                repeat_map[i + k] = "D"
                repeat_map[j + k] = "D"
            j = sequence.find(block, j + 1)

    duplicate_zones = sum(1 for value in repeat_map if value == "D")

    for i in range(strand_length - 7):
        window = sequence[i : i + 8]
        if all(ch in {"A", "U"} for ch in window):
            pattern_repeats += 1
            for k in range(8):
                repeat_map[i + k] = "W"
        if all(ch in {"C", "G"} for ch in window):
            pattern_repeats += 1
            for k in range(8):
                repeat_map[i + k] = "S"

    for i in range(strand_length - 4):
        if sequence[i] == sequence[i + 1] == sequence[i + 2] == sequence[i + 3] == sequence[i + 4]:
            poly_repeats += 1
            for k in range(5):
                repeat_map[i + k] = sequence[i]

    restriction_motifs = [
        "GGUCUC",
        "GAGACC",
        "GAAGAC",
        "GUCUUC",
        "CGUCUC",
        "GAGACG",
        "GCUCUUC",
        "GAAGAGC",
        "AUCUGUU",
    ]
    for motif in restriction_motifs:
        j = sequence.find(motif)
        while j != -1:
            restriction_sites += 1
            for k in range(len(motif)):
                repeat_map[j + k] = "X"
            j = sequence.find(motif, j + 1)

    return repeat_map, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites


def build_barriers(structure_map, map_array, sequence_length):
    barriers = ["·"] * sequence_length
    topo_count = 0
    for i, ch in enumerate(structure_map):
        if ch == ".":
            barriers[i] = "·"
            topo_count = 0
        elif ch == "(":
            barriers[i] = "x"
            topo_count = 0
        elif ch == ")":
            partner = map_array[i]
            if partner < 0 or partner >= sequence_length:
                continue
            if barriers[partner] == "x":
                barriers[i] = "·"
                barriers[partner] = "·"
                topo_count = 0
            elif barriers[partner] == "X":
                if topo_count > 5:
                    barriers[i] = "X"
                    barriers[partner] = "~"
                else:
                    barriers[i] = "~"
                    barriers[partner] = "~"
                topo_count += 1
        if i > KL_DELAY and structure_map[i - KL_DELAY] == "]":
            partner = map_array[i - KL_DELAY]
            if 0 <= partner < sequence_length:
                barriers[i - KL_DELAY] = "·"
                barriers[partner] = "·"
                for k in range(partner, i - KL_DELAY):
                    if barriers[k] == "x":
                        barriers[k] = "X"
    return barriers


def render_structure_cell(ch, grid=None, i=None, j=None):
    if ch == "5" or ch == "3":
        return ch
    if ch == "T":
        return "─"
    if ch == " ":
        return " "
    if ch == "7":
        return "╮"
    if ch == "-":
        return "─"
    if ch == "r":
        return "╯"
    if ch == "L":
        return "╰"
    if ch == "J":
        return "╭"
    if ch == "p":
        if grid is None or i is None or j is None:
            return "┊"
        above = get_pattern_char(grid, i + 1, j)
        below = get_pattern_char(grid, i - 1, j)
        if (above, below) in {("G", "C"), ("C", "G"), ("A", "U"), ("U", "A"), ("G", "U"), ("U", "G")}:
            return "┊"
        return "?"
    if ch == "b":
        if grid is None or i is None or j is None:
            return "="
        right = get_pattern_char(grid, i, j + 1)
        left = get_pattern_char(grid, i, j - 1)
        if (right, left) in {("G", "C"), ("C", "G"), ("A", "U"), ("U", "A"), ("G", "U"), ("U", "G")}:
            return "="
        return "?"
    if ch == "i":
        return "┊"
    if ch == "x":
        return "╴"
    if ch == "!":
        return "!"
    return ch


def render_strand_cell(ch, grid, i, j, strand_dir):
    if ch == "5" or ch == "3":
        return ch
    if ch == "T":
        return "─"
    if ch == " ":
        return " "
    if ch == "7":
        return "╮"
    if ch == "-":
        return "─"
    if ch == "r":
        return "╯"
    if ch == "L":
        return "╰"
    if ch == "J":
        return "╭"
    if ch == "x":
        return "╴"
    if ch == "i":
        return "┊"
    if ch == "b":
        return "─"
    if ch == "p" or ch == "!" or ch == "*":
        direction = strand_dir.get((i, j), "right")
        if direction in {"up", "down"}:
            return "┊"
        return "─"
    if ch in NUCLEOTIDE_CHARS:
        direction = strand_dir.get((i, j), "right")
        if direction in {"up", "down"}:
            return "┊"
        return "─"
    return ch


def render_highlight_cell(ch, repeat_map, n_map, i, j):
    if ch in NUCLEOTIDE_CHARS or ch in "ACGUTNXY":
        idx = n_map.get((i, j), None)
        if idx is not None and 1 <= idx <= len(repeat_map):
            return repeat_map[idx - 1]
    return render_structure_cell(ch, None, i, j)


def render_wobble_cell(ch, wobbles_seq, n_map, i, j):
    if ch in NUCLEOTIDE_CHARS:
        idx = n_map.get((i, j), None)
        if idx is not None and 1 <= idx <= len(wobbles_seq):
            return wobbles_seq[idx - 1]
    return render_structure_cell(ch, None, i, j)


def render_barrier_cell(ch, barriers, n_map, i, j):
    if ch in NUCLEOTIDE_CHARS:
        idx = n_map.get((i, j), None)
        if idx is not None and 1 <= idx <= len(barriers):
            return barriers[idx - 1]
    return render_structure_cell(ch, None, i, j)


def structure_printer(output, grid, seq_output:str, repeat_map:list, wobbles_seq:list, barriers:list,complement_zones:int, duplicate_zones:int, pattern_repeats:int, poly_repeats:int, restriction_sites:int,n_map:dict,strand_dir:dict):
        output.write("2D diagram with sequence\n")
        for i in range(grid.shape[0]):
            row_chars = [render_structure_cell(get_pattern_char(grid, i, j), grid, i, j) for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

        output.write("\n\nStrand Path\n")
        for i in range(grid.shape[0]):
            row_chars = [render_strand_cell(get_pattern_char(grid, i, j), grid, i, j, strand_dir) for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

        output.write("\n")
        sequence_array = list(seq_output)
        sequence_check = all(ch in VALID_BASES for ch in sequence_array)
        if not sequence_check:
            output.write("\nSequence not suitable for pattern search.  Must only contain A, U C and G. \n")
        else:
            output.write("\n\nHighlighting Repeat Sequences \n\n")
            output.write(f" WC complement region (P) {COMPLEMENT_WINDOW} or longer: {complement_zones} nts\n")
            output.write(f" Duplicated region (D) {DUPLICATE_WINDOW} or longer: {duplicate_zones} nts\n")
            output.write(f" Strong/Weak region (S/W) 8 or longer: {pattern_repeats} nts\n")
            output.write(f" 5 or more in a row of the same nucleotide (A,U,C,G): {poly_repeats} nts\n")
            output.write(f" Common restriction site (X): {restriction_sites} nts\n")
            output.write("\n")
            for i in range(grid.shape[0]):
                row_chars = []
                for j in range(grid.shape[1]):
                    ch = get_pattern_char(grid, i, j)
                    if ch in NUCLEOTIDE_CHARS:
                        row_chars.append(render_highlight_cell(ch, repeat_map, n_map, i, j))
                    else:
                        row_chars.append(render_structure_cell(ch, grid, i, j))
                output.write("".join(row_chars) + "\n")

        output.write("\n\nHighlighting GU Pairs\n")
        for i in range(grid.shape[0]):
            row_chars = []
            for j in range(grid.shape[1]):
                ch = get_pattern_char(grid, i, j)
                if ch in NUCLEOTIDE_CHARS:
                    row_chars.append(render_wobble_cell(ch, wobbles_seq, n_map, i, j))
                else:
                    row_chars.append(render_structure_cell(ch, grid, i, j))
            output.write("".join(row_chars) + "\n")

        output.write("\n\nHighlighting Structural Barriers\n\n")
        for i in range(grid.shape[0]):
            row_chars = []
            for j in range(grid.shape[1]):
                ch = get_pattern_char(grid, i, j)
                if ch in NUCLEOTIDE_CHARS:
                    row_chars.append(render_barrier_cell(ch, barriers, n_map, i, j))
                else:
                    row_chars.append(render_structure_cell(ch, grid, i, j))
            output.write("".join(row_chars) + "\n")
