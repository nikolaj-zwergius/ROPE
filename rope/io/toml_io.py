from pathlib import Path
from typing import Any

try: import tomllib
except ImportError:
    import tomli as tomllib


def load_toml(package_path: str | Path) -> dict[str, Any]:
    with open(package_path, "rb") as f:
        data = tomllib.load(f)

    return data