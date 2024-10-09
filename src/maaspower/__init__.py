"""
maaspower package
=================
"""

"""Top level API.

.. data:: __version__
    :type: str

    Version number as calculated by https://github.com/pypa/setuptools_scm
"""

from ._version import __version__  # noqa: E402

# __all__ defines the public API for the package.
# Each module also defines its own __all__.
__all__ = ["__version__", "maasconfig", "webhook"]
