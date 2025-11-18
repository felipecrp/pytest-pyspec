"""
Decorators that let users override pyspec descriptions directly in tests.

Each decorator stores the provided text on the decorated callable or class so
the tree builder can favor it over docstrings/identifiers.
"""
from __future__ import annotations

from typing import Callable, TypeVar, Union

T = TypeVar('T', bound=Union[Callable[..., object], type])

# Attribute names used by the semantic tree.
DESCRIPTION_ATTR = '__pyspec_description__'
DECORATOR_ATTR = '__pyspec_decorator__'


def _apply_decorator(target: T, description: str, decorator: str) -> T:
    """
    Store metadata on the decorated object.
    """
    cleaned = description.strip()
    if not cleaned:
        raise ValueError("pyspec decorators require a non-empty description")
    setattr(target, DESCRIPTION_ATTR, cleaned)
    setattr(target, DECORATOR_ATTR, decorator)
    return target


def _build_decorator(decorator: str) -> Callable[[str], Callable[[T], T]]:
    """
    Factory for decorators that capture a human-friendly description.
    """
    def decorator(description: str) -> Callable[[T], T]:
        def wrapper(target: T) -> T:
            return _apply_decorator(target, description, decorator)
        return wrapper
    return decorator


# Public decorators. ``with`` is a reserved keyword, so we expose ``with_``.
describe = _build_decorator('describe')
with_ = _build_decorator('with')
without = _build_decorator('without')
when = _build_decorator('when')
it = _build_decorator('it')


__all__ = [
    'describe',
    'with_',
    'without',
    'when',
    'it',
    'DESCRIPTION_ATTR',
    'DECORATOR_ATTR',
]
