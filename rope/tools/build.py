import os
#from rope.definitions.modules import named_module_libary
import argparse
from rope.core.Build_logic import RNAbuild
from rope.utils.cli_helper import WideFormatter
from rope.model.ModuleCache import ModuleCache
from rope.io.index_handler import load_index, load_variant_index

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Build PDB files from blueprint",
    formatter_class=WideFormatter,
    prog="rope-build",
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--config",
        help="Configuration TOML file"
    )
    group.add_argument(
        "--ligand",
        action="append",
        metavar="MODULE=LIGAND",
        help="Select ligand variant"
    )
    parser.add_argument(
        "blueprint",
        nargs="*",
        help="Blueprint file"
    )
    

    parser.add_argument(
        "--list",
        nargs="?",
        const="all",
        metavar="MODULE",
        help="Show avaliable ligands for a givin module, if none givin show all"
    )



    return parser

def ligand_switcher(args)-> dict[str,str]:
    ligands = {}
    if args.config:
        pass
    elif args.ligand:
        for i in args.ligand:
            name,option = i.split("=")
            ligands[name] = option

    return ligands


def ligand_print(args,index):
    variants = load_variant_index()
    if args.list == "all":
        for i in index:
            print(f"{index[i].name}:")
            if index[i].symbol not in variants:
                continue

            for ligand in variants[index[i].symbol]:
                print(f"    {ligand}")

            print()
            raise SystemExit(0)

    elif args.list:
        module = ""
        for i in index:
            if index[i].name == args.list:
                module = index[i]
        else:
            if not module:
                raise Exception
        print(f"{module.name}:")
        for i in variants[module.symbol]:
            print(f"    {i}")
        raise SystemExit(0)

def main():
    args = build_parser().parse_args()
    wd = os.getcwd()
    folder = f"{wd}/RNAbuild"
    index_library = load_index()
    modulecahce = ModuleCache(index_library)
    ligand_print(args,index_library)
    ligands = {}
    ligands = ligand_switcher(args)
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not args.blueprint:
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb",modulecahce,index_library,ligands)
    else:
        for file in args.blueprint:
            file = str(file.lstrip(f".{chr(92)}"))
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split(".")[:-1]}")
                continue
            if file in os.listdir():
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb",modulecahce,index_library,ligands)
            else:
                print(f"{file} not found in folder")

if __name__ == "__main__":
    main()
