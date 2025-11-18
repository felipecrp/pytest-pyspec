"""
Public package interface for pytest-pyspec.

Re-export decorator helpers so users can simply::

    from pytest_pyspec import describe, it

instead of importing from ``pytest_pyspec.decorators``.
"""

from .decorators import describe, it, when, with_, without

__all__ = [
    'describe',
    'with_',
    'without',
    'when',
    'it',
]
