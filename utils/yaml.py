import yaml


def parse_yaml_file(path: str):
    with open(path, "r") as f:
        content = yaml.full_load(f)
    return content
