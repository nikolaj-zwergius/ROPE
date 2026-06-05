"""Clean RNA_lib PDB files.

This module walks the RNA_lib directory tree, removes any lines that are not
ATOM/HETATM records, and normalizes atom names to the standard nucleotide
library names.
"""

import os

STANDARD_ATOM_NAME_MAP = {
    'O1P': 'OP1',
    'O2P': 'OP2',
    'C4*': "C4'",
}

STANDARD_ATOM_NAMES = {
    'P', "OP1", "OP2",
    "O5'", "C5'", "C4'", "C3'", "O3'", "O4'", "C1'", "C2'",
    'N1', 'C2', 'N3', 'C4', 'C5', 'C6',
    'N9', 'C8', 'N7',
    'N2', 'N4', 'N6', 'O2', 'O4', 'O6',
}


def _is_pdb_atom_line(line: str) -> bool:
    return line[:6].strip() in {'ATOM', 'HETATM'}


def _normalize_atom_name(atom_name: str) -> str:
    name = atom_name.strip()
    if not name:
        return atom_name
    return STANDARD_ATOM_NAME_MAP.get(name, name)


def _format_pdb_atom_name(atom_name: str) -> str:
    """Format an atom name into the 4-character PDB atom name field."""
    normalized = _normalize_atom_name(atom_name).replace('*', "'")
    if len(normalized) >= 4:
        return normalized[:4]
    if normalized and normalized[0].isdigit():
        return normalized.ljust(4)
    return f" {normalized:<3}"


def _slice_field(line: str, start: int, end: int) -> str:
    return line[start:end] if len(line) >= end else line[start:].ljust(end - start)


def _format_pdb_atom_line(line: str) -> str:
    record_name = _slice_field(line, 0, 6).strip()
    serial = _slice_field(line, 6, 11).strip()
    atom_name = _slice_field(line, 12, 16)
    alt_loc = _slice_field(line, 16, 17)
    res_name = _slice_field(line, 17, 20).strip()
    chain_id = _slice_field(line, 21, 22)
    res_seq = _slice_field(line, 22, 26).strip()
    i_code = _slice_field(line, 26, 27)
    x = _slice_field(line, 30, 38).strip()
    y = _slice_field(line, 38, 46).strip()
    z = _slice_field(line, 46, 54).strip()
    occupancy = _slice_field(line, 54, 60).strip()
    temp_factor = _slice_field(line, 60, 66).strip()
    element = _slice_field(line, 76, 78).strip()
    charge = _slice_field(line, 78, 80).strip()

    return (
        f"{record_name:<6}"
        f"{serial:>5} "
        f"{_format_pdb_atom_name(atom_name)}"
        f"{alt_loc:1}"
        f"{res_name:<3} "
        f"{chain_id:1}"
        f"{res_seq:>4}"
        f"{i_code:1}   "
        f"{x:>8}"
        f"{y:>8}"
        f"{z:>8}"
        f"{occupancy:>6}"
        f"{temp_factor:>6}"
        f"          {element:>2}{charge:>2}\n"
    )


def clean_pdb_file(file_path: str) -> None:
    """Clean a single PDB file in place."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as reader:
        original_lines = reader.readlines()

    cleaned_lines = []
    for line in original_lines:
        if not _is_pdb_atom_line(line):
            continue
        cleaned_lines.append(_format_pdb_atom_line(line))

    if cleaned_lines != original_lines:
        with open(file_path, 'w', encoding='utf-8') as writer:
            writer.writelines(cleaned_lines)


def clean_rna_lib_pdb_files(root_dir: str | None = None) -> None:
    """Recursively clean all PDB files under the RNA_lib directory."""
    if root_dir is None:
        root_dir = os.path.dirname(__file__)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdb'):
                clean_pdb_file(os.path.join(dirpath, filename))


if __name__ == '__main__':
    clean_rna_lib_pdb_files()
