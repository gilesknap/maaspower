"""
globals.py
----------

A few global defintions
"""

from enum import Enum
from typing import Any, TypeVar

from apischema import schema

#: A generic Type for use in type hints
T = TypeVar("T")

maas_config: Any = None


class MaasResponse(Enum):
    """Default  responses understood by the MAAS query webhook calls"""

    on = "status : running"
    off = "status : stopped"
    ok = "status: ok"


def desc(description: str):
    """a description Annotation to provide tooltips in the YAML editor"""
    return schema(description=description)
