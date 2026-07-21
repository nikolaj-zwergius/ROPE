from rope.io.pakage_disover import find_pakages
import tomllib

def load_toml(package_path):
    with open(package_path, "rb") as f:
        data = tomllib.load(f)

    return data