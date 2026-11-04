from os import listdir
from pathlib import Path


def find_packages() -> tuple[list[Path], list[Path], list[Path], list[Path]]:
    """Discover module TOML files and unexpected files in the RNA library.

    Returns ``(packages, root_files, type_files, missing_toml)``. Package and
    missing-TOML paths point to ``module.toml`` locations; the other lists
    contain files directly under the library root or a module-type directory.
    Directory traversal follows filesystem order rather than sorting entries.
    """
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