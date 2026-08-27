
from pathlib import Path
try: import tomllib
except ImportError:
    import tomli as tomllib


def get_version() -> str:
    pyproject = Path(__file__).parents[1] / "pyproject.toml"

    data = tomllib.loads(pyproject.read_text())

    return data["project"]["version"]