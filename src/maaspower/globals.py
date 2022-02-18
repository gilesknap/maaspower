"""
A few global defintions
"""
from typing import TypeVar

from apischema import schema

#: A generic Type for use in type hints
T = TypeVar("T")


def desc(description: str):
    """a description Annotation to provide tooltips in the YAML editor"""
    return schema(description=description)
