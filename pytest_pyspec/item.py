from types import ModuleType
from typing import Dict, List

import re

import pytest

class Item:
    """
    Wrapper around a pytest.Item that provides a human-friendly description.

    Responsibilities:
    - Derive a readable description for a test or container from either the
      docstring of the underlying object or its Python name.
    - Provide helpers to normalize names (convert CamelCase/snake_case into
      words), strip common pytest prefixes, and keep a consistent
      representation.
    """

    def __init__(self, item: pytest.Item) -> None:
        self._item = item

    @property
    def description(self) -> str:
        """
        Return a human-readable description for the wrapped pytest item.

        Preference order:
        1) First non-empty line of the object's docstring, stripped.
        2) A description derived from the Python name of the item.
        """
        docstring = getattr(self._item.obj, "__doc__", None)
        if docstring:
            return self._parse_docstring(docstring)
        return self._parse_itemname(self._item.name)

    def _parse_docstring(self, docstring: str) -> str:
        """
        Return the first line of a docstring, trimmed of surrounding spaces.
        """
        first_line = docstring.splitlines()[0]
        return first_line.strip()

    def _parse_name(self, name: str) -> str:
        """
        Normalize a Python identifier into words.

        Steps:
        - Insert underscores before internal capital letters (turn "MyClass"
          -> "My_Class").
        - Lowercase everything.
        - Replace underscores with single spaces and normalize multiple
          underscores.
        """
        description = re.sub(
            r'(?!^[A-Z])([A-Z])',
            r'_\g<1>',
            name,
        )
        description = description.lower()
        description = ' '.join(description.split('_'))
        return description

    def _parse_itemname(self, name: str) -> str:
        """
        Create a description from a pytest test function name.

        - Uses _parse_name to normalize the identifier.
        - Removes common prefixes like "test"/"it".
        """
        description = self._parse_name(name)
        description = re.sub(
            r'^(test|it) ',
            '',
            description,
        )
        return description

    def __repr__(self) -> str:
        return self._item.__repr__()


class Test(Item):
    """
    Represents a single test item and its relationship to a container.
    """
    def __init__(self, item: pytest.Item) -> None:
        super().__init__(item)
        self.container: Container = None
        self.outcome: str = None

    @property
    def level(self) -> int:
        """
        Depth in the container hierarchy (root container is 0).
        """
        if not self.container:
            return 0
        return self.container.level +1
   
    
class Container(Item):
    """
    Represents a grouping of tests (e.g., class/function scopes) in pytest.

    Tracks:
    - Nested containers (parents/children) following pytest's item tree.
    - Contained tests.
    Provides utilities to compute display names and levels.
    """
    def __init__(self, item: pytest.Item) -> None:
        super().__init__(item)
        self.tests: List[Test] = list()
        self.containers: List[Container] = list()
        self.parent = None

    def add(self, test: Test) -> None:
        """
        Attach a Test to this container and set its back-reference.
        """
        self.tests.append(test)
        test.container = self

    def add_container(self, container: 'Container') -> None:
        """
        Attach a child container and set parent back-reference.
        """
        self.containers.append(container)
        container.parent = self

    def flat_list(self) -> list:
        """
        Return a list of containers from root to self.
        """
        containers = []
        container = self
        while container:
            containers.insert(0, container)
            container = container.parent
        return containers

    @property
    def level(self) -> int:
        """
        Compute this container's depth relative to the module root.

        Walks up pytest's internal node tree until reaching a ModuleType parent.
        """
        level = 0
        
        item = self._item
        # Climb the pytest node hierarchy until we reach the module node
        while item.parent and not isinstance(item.parent.obj, ModuleType):
            level += 1
            item = item.parent
        
        return level
    
    def _parse_docstring(self, docstring: str) -> str:
        """
        Parse container docstring and prepend an article when appropriate.

        If the first word doesn't start with "with"/"without", prefix with
        "a ". This mirrors RSpec-style descriptions like "a function" vs
        "with options".
        """
        description = super()._parse_docstring(docstring)
        if not description.startswith(('with ', 'without ')):
            description = f'a {description}'
        return description
    
    def _parse_itemname(self, name: str) -> str:
        """
        Create a container description from a pytest node name.

        - Normalize the identifier into words.
        - Replace leading "test"/"describe" with the article "a ".
        """
        description = self._parse_name(name)
        description = re.sub(
            r'^([Tt]est|[Dd]escribe) ',
            'a ',
            description)
        return description


class ItemFactory:
    """
    Factory responsible for creating Test items and wiring them into containers.
    """
    def __init__(self) -> None:
        self.container_factory = ContainerFactory()

    def create(self, item: pytest.Item) -> Test:
        """
        Wrap a pytest item as a Test and attach it to its Container.

        Also mutates pytest's item name to the human-readable description for
        reporting.
        """
        test_item = Test(item)

        container_item = item.parent
        container = self.container_factory.create(container_item)
        if container:
            container.add(test_item)       

        item.name = test_item.description
        return test_item
        

class ContainerFactory:
    """
    Factory that ensures containers are unique per pytest node and linked
    properly.
    """
    def __init__(self) -> None:
        self.containers: Dict[str, Container] = dict()

    def create(self, item: pytest.Item) -> 'Container':
        """
        Create (or fetch) the deepest Container for a given pytest node.
        """
        containers = self._create_containers(item)
        if not containers:
            return None

        return containers[-1]
    
    def _create_unique_container(self, item: pytest.Item) -> 'Container':
        """
        Return a unique Container for a pytest node, creating if absent.

        Also sets the pytest node's display name to the container description.
        """
        # Cache containers per pytest node to keep uniqueness
        if item not in self.containers:
            container = Container(item)
            self.containers[item] = container

        container = self.containers.get(item)
        # Mutate node's visible name to our human-friendly description
        item.name = container.description
        return container

    def _create_containers(self, item: pytest.Item) -> list:
        """
        Build the chain of containers from a pytest node up to the module root.
        """
        containers = []
        child_container = None
        # Walk upwards creating/collecting containers until the module level
        while item and not isinstance(item.obj, ModuleType):
            container = self._create_unique_container(item)
            # Link the previous (deeper) container as a child of the current one
            if child_container:
                container.add_container(child_container)

            containers.insert(0, container)
            child_container = container
            item = item.parent
        return containers