"""Contains utility functions, e.g. for patching JSON files."""

import json
import pathlib
import subprocess
from os import PathLike, listdir, path
from typing import Dict, Union

import yaml

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOCALES_FOLDER_PATH = ROOT_PATH / "web/public/locales/"
LOCALE_FILE_PATHS = [
    LOCALES_FOLDER_PATH / f
    for f in listdir(LOCALES_FOLDER_PATH)
    if path.isfile(LOCALES_FOLDER_PATH / f) and f.endswith(".json")
]


def run_shell_command(cmd: str, cwd: PathLike | str = "") -> str:
    return subprocess.check_output(cmd, shell=True, encoding="utf8", cwd=cwd).rstrip(
        "\n"
    )


class JsonFilePatcher:
    """
    A helping hand to patch JSON files.

    Example:

    with JsonFilePatcher(ROOT_PATH / "web/geo/world.geojson") as f:
        if zone in f.content:
            del f.content[zone]
    """

    def __init__(self, file_path: PathLike | str, indent: int | None = 2):
        self.file_path = file_path
        self.indent = indent

    def __enter__(self):
        with open(self.file_path) as f:
            self.content: dict = json.load(f)

        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            raise

        with open(self.file_path, "w") as f:
            json.dump(
                self.content,
                f,
                indent=self.indent,
                ensure_ascii=False,
            )
            # TODO: enable sort_keys=True
            f.write("\n")

        print(f"🧹 Patched {self.file_path.relative_to(ROOT_PATH)}")


class YamlFilePatcher(object):
    """
    A helping hand to patch YAML files.

    Example:

    with YamlFilePatcher(ROOT_PATH / "web/geo/world.yaml") as f:
        if zone in f.content:
            del f.content[zone]
    """

    def __init__(self, file_path: Union[PathLike, str]):
        self.file_path = file_path

    def __enter__(self):
        self.content: Dict = yaml.safe_load(open(self.file_path, encoding="utf-8"))

        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            raise

        with open(self.file_path, "w") as f:
            f.write(yaml.dump(self.content, default_flow_style=False))
        print(f"🧹 Patched {self.file_path.relative_to(ROOT_PATH)}")
