"""Clean RNA_lib PDB files.

This module walks the RNA_lib directory tree, removes any lines that are not
ATOM/HETATM records, and normalizes atom names to the standard nucleotide
library names.
"""

from pathlib import Path
from rope.definitions.rope_def import ROOT
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


def _format_pdb_atom_line(line: str,current_res:int,res_index:int) -> tuple[str,int,int]:
    record_name = _slice_field(line, 0, 6).strip()
    serial = _slice_field(line, 6, 11).strip()
    atom_name = _slice_field(line, 12, 16)
    alt_loc = _slice_field(line, 16, 17)
    res_name = _slice_field(line, 17, 20).strip()
    chain_id = "A"
    res_seq = _slice_field(line, 22, 26).strip()
    if current_res != int(res_seq):
        res_index += 1
        current_res = int(res_seq)
    res_seq = res_index
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
    ),current_res,res_index


def clean_pdb_file(file_path: Path) -> None:
    """Clean a single PDB file in place."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as reader:
        original_lines = reader.readlines()
    current_res = 0
    res_index = 0
    cleaned_lines = []
    for line in original_lines:
        if not _is_pdb_atom_line(line):
            continue
        line, current_res, res_index = _format_pdb_atom_line(line,current_res,res_index)
        cleaned_lines.append(line)

    if cleaned_lines != original_lines:
        with open(file_path, 'w', encoding='utf-8') as writer:
            writer.writelines(cleaned_lines)


def clean_rna_lib_pdb_files(root_dir: Path | None = None) -> None:
    """Recursively clean all PDB files under the RNA_lib directory."""
    if root_dir is None:
        root_dir = ROOT/"data/RNA_lib/modules"
    dirs = os.listdir(root_dir)  
    print(dirs)
    for folder in dirs:
        path = Path(root_dir)/folder
        for modules in os.listdir(path):
            pdb_path = path/modules
            for file in os.listdir(pdb_path):
                if file.endswith(".pdb"):
                    clean_pdb_file(pdb_path/file)


if __name__ == '__main__':
    clean_rna_lib_pdb_files()
