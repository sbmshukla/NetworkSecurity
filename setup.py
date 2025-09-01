"""
setup.py — Build script for packaging and distributing the 'eduscore' project.
Adapted for a network security context: useful for IDS tools, secure pipelines, or encrypted utilities.
"""

from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    Reads dependencies from requirements.txt.
    Cleans up entries and removes editable install flag (-e .), which is used during local dev.
    Ideal for reproducible builds in secure environments.
    """
    try:
        with open(file_path) as f:
            requirements = [line.strip() for line in f if line.strip()]
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
        return requirements
    except FileNotFoundError:
        print(f"File Not Found!")
        return []


setup(
    name="Network Security",
    version="0.0.1",
    author="sbmshukla",
    author_email="sbmshukla17@gmail.com",
    packages=find_packages(),  # Auto-discovers all Python packages/modules
    install_requires=get_requirements("requirements.txt"),
)
