"""
A few global defintions
"""
from enum import Enum
from typing import TypeVar

from apischema import schema

#: A generic Type for use in type hints
T = TypeVar("T")


class MaasResponse(Enum):
    on = "status : running"
    off = "status : stopped"
    ok = "status: ok"


def desc(description: str):
    """a description Annotation to provide tooltips in the YAML editor"""
    return schema(description=description)
