import argparse
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


def fail(msg: str) -> NoReturn:
    print(f"\n❌ Error: {msg}")
    sys.exit(1)


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        fail(f"Command failed: {' '.join(cmd)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install ROPE."
    )

    parser.add_argument(
            "--pip",
            choices=["pip", "pipx"],
            default="pip",
            help="Pick install tool (default: pip)",
        )

    parser.add_argument(
        "--mode",
        choices=["edit", "normal"],
        default="normal",
        help="Install mode (default: normal). Use 'edit' for an editable installation, which is useful for development.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Pass the --force flag to pip or pipx. This is useful when reinstalling with pipx."
    )


    args = parser.parse_args()


    print("\n------------------------------")
    print(f"Installer : {args.pip}")
    print(f"Mode      : {args.mode}")
    print(f"Forced    : {args.force}")
    print("------------------------------\n")

    python = sys.executable

    # ----------------------
    # Install logic
    # ----------------------
    if args.pip == "pipx":
        print("📦 Installing with pipx...")

        # Check pipx exists
        if not shutil.which("pipx"):
            fail("pipx not found")
        install_logic_rope =  ["pipx", "install"]
        if args.mode == "edit":
            install_logic_rope.append("--editable")
        if args.force:
            install_logic_rope.append("--force")

        install_logic_rope.extend(["."])
        run(install_logic_rope)

    else:
        print("📦 Installing with pip...")

        install_logic_rope =  [python, "-m", "pip", "install"]
        if args.mode == "edit":
            install_logic_rope.append("-e")

        install_logic_rope.extend(["."])

        run(install_logic_rope)

    print("\n✅ Installation complete\n")


if __name__ == "__main__":
    import shutil
    main()
