import os
import shutil


def copy_file(source: str, destination: str, create_directories: bool = False) -> None:
    destination_dir = os.path.dirname(destination)
    if create_directories:
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
    shutil.copyfile(source, destination)


def read_file(path: str) -> str:
    with open(path, "r") as f:
        content = f.read()
    return content


def write_to_file(content: str, file_path: str, create_directories: bool = False) -> None:
    dir_path = os.path.dirname(file_path)
    if create_directories:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    with open(file_path, "w") as f:
        f.write(content)
