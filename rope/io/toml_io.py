try: import tomllib
except ImportError:
    import tomli as tomllib

def load_toml(package_path):
    with open(package_path, "rb") as f:
        data = tomllib.load(f)

    return data