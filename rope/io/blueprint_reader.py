from pathlib import Path


def read_sequence_file(path: str | Path) -> str:
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith(">"):
                continue
            lines.append(line)
    return "".join(line.strip() for line in lines).upper()


def parse_header(file_path: str | Path) -> tuple[str, str]:
    name = "Untitled"
    kl_pattern = ""
    with open(file_path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(">"):
                name = line[1:33].strip()
            elif line.startswith("@"):
                kl_pattern = line[1:33].strip()
    return name, kl_pattern