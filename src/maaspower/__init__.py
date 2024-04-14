"""
maaspower package
=================
"""

from importlib.metadata import version

from . import maasconfig, webhook

__version__ = version("maaspower")
del version


# __all__ defines the public API for the package.
# Each module also defines its own __all__.
__all__ = ["__version__", "maasconfig", "webhook"]
