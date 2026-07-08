import os
from rope.definitions.modules import named_module_libary
import argparse
from rope.core.Build_logic import RNAbuild
from rope.utils.parser_herlper import WideFormatter



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
            named_module_libary[name].set_variant(option)
            ligands[name] = option

    return ligands


def ligand_print(args):
    if args.list == "all":
        for module in named_module_libary.values():
            print(f"{module.name}:")
            if not module.ligand_variants:
                continue

            for ligand in module.ligand_variants:
                print(f"    {ligand}")

            print()
            raise SystemExit(0)

    elif args.list:
        module = named_module_libary[args.list]
        print(f"{module.name}:")
        print()
        for i in module.variants.keys():
            print(f"\t {i}")
        raise SystemExit(0)

def main():
    args = build_parser().parse_args()
    ligand_print(args)
    ligands = {}
    ligands = ligand_switcher(args)
    wd = os.getcwd()
    folder = f"{wd}/RNAbuild"
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not args.blueprint:
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb",ligands)
    else:
        for file in args.blueprint:
            file = str(file.lstrip(f".{chr(92)}"))
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split(".")[:-1]}")
                continue
            if file in os.listdir():
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb",ligands)
            else:
                print(f"{file} not found in folder")

if __name__ == "__main__":
    main()
