
from .item import Container, Test


def print_container(container: Container):
    output = "\n"
    for container in container.flat_list():
        output += print_parent_container(container)
        container = container.parent

    # ident = "  " * container.level
    # output = f"\n\n{ident}{container.description}"
    return output

def print_parent_container(container: Container):
    ident = "  " * container.level
    output = f"\n{ident}{container.description}"
    return output

def print_test(test: Test):
    ident = "  " * test.level
    output = f"\n{ident}{test.description}"
    return output