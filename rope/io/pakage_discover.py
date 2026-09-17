from os import listdir
from pathlib import Path

def find_pakages() -> tuple[list[Path],list[Path],list[Path],list[Path]]:
    found = []
    missing_toml = []
    root_files = []
    type_files = []

    PROGRAM_DIR = Path(__file__).resolve().parent.parent
    folder_path = Path(PROGRAM_DIR/"data"/"RNA_lib/modules")
    for type_dir in listdir(folder_path):
        type_path = folder_path/type_dir
        if type_path.is_file():
            root_files.append(type_path)
            continue
        for module_dir in listdir(type_path):
            module_path = type_path/module_dir
            if module_path.is_file():
                type_files.append(module_path)
                continue
            toml = module_path/"module.toml"
            if not toml.exists():
                missing_toml.append(toml)
                continue
            found.append(toml)
    return found ,root_files,type_files,missing_toml