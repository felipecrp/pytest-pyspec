import pytest
from .item import Container, Test


def print_container(container: Container) -> str:
    output = "\n"
    if container:
        for container in container.flat_list():
            output += print_parent_container(container)
            container = container.parent
    return output

def print_parent_container(container: Container) -> str:
    ident = "  " * container.level
    output = f"\n{ident}{container.description}"
    return output

def print_test(test: Test) -> str:
    ident = "  " * test.level
    status = print_test_status(test)
    output = f"\n{ident}{status} {test.description}"
    return output

def print_test_status(test: Test) -> str:
    if test.outcome == 'passed':
        return '✓'
    elif test.outcome == 'failed':
        return '✗'
    else:
        return '»'
