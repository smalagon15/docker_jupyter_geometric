from setuptools import setup, find_packages
from pathlib import Path
from typing import List
import re
import os

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).resolve()
REQUIREMENTS_PATH = Path(ROOT_PATH, "requirements.txt")
# Load requirements from a file name in local directory
def load_requirements(fname: str):
    txt = open(fname, "r")
    requirements = txt.read().splitlines()
    txt.close()
    return requirements
    
def parse_requirements(requirements: Path) -> List[str]:
    with requirements.open(mode="r") as fd:

        rlist_sans_comments = [
            line.strip()
            for line in fd.read().split("\n")
            if (line.strip() or line.strip().startswith("#"))
        ]

        final_rlist = [
            line
            if not re.match(
                pattern=r"^https?://.*$",
                string=line)
            else re.sub(
                pattern=r"(.*(?:https?://.*/)([a-zA-Z0-9_].*)[-]([a-zA-Z0-9.]*)([.]tar[.]gz|[.]tgz).*)",
                repl=r"\2 @ \1",
                string=line
            )
            for line in rlist_sans_comments
        ]

    return final_rlist

# This is a function to combs the project directory recusively and install sub folders
# Because this is recursive it intitially starts with the same parameters
def package_directory(directory: str, parent_package: str):
    packages = [parent_package]
    for (_, directories, _) in os.walk(directory):
        if "__pycache__" in directories:
            directories.remove("__pycache__")
            if len(directories) == 0:
                return packages
            else:
                for folder in directories:
                    sub_package = parent_package + "." + folder
                    packages = packages + package_directory(os.path.join(directory, folder), sub_package)
    return packages

# calls the function package_directory
setup_packages = package_directory("Neo4jDriver","Neo4jDriver")
setup(name='Neo4jDriver',
      version='1.0',
      description='Neo4jDriver 1.0',
      packages=find_packages(),
      install_requires=parse_requirements(REQUIREMENTS_PATH)
     )