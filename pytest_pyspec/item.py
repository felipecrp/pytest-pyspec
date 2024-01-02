from types import ModuleType
from typing import Dict, List

import re

import pytest


class Item:
    def __init__(self, item: pytest.Item) -> None:
        self._item = item

    @property
    def description(self):        
        docstring = self._item.obj.__doc__
        if docstring:
            return self._parse_docstring(docstring)
        return self._parse_itemname(self._item.name)

    def _parse_docstring(self, docstring):
        description = docstring.splitlines()[0]
        description = description.strip()
        return description

    def _parse_name(self, name):
        description = re.sub(
            r'(?!^[A-Z])([A-Z])',
            r'_\g<1>',
            name)
        description = description.lower() 
        description = ' '.join(description.split('_'))
        return description
    
    def _parse_itemname(self, name):
        description = self._parse_name(name)
        description = re.sub(
            r'^(test|it) ',
            '',
            description)
        return description

    def __repr__(self):
        return self._item.__repr__()


class Test(Item):
    def __init__(self, item: pytest.Item) -> None:
        super().__init__(item)
        self.container: Container = None
        self.outcome: str = None

    @property
    def level(self) -> int:
        if not self.container:
            return 0
        return self.container.level +1
   
    
class Container(Item):
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.tests: List[Test] = list()
        self.containers: List[Container] = list()
        self.parent = None

    def add(self, test: Test):
        self.tests.append(test)
        test.container = self

    def add_container(self, container: 'Container'):
        self.containers.append(container)
        container.parent = self

    def flat_list(self):
        containers = []
        container = self
        while container:
            containers.insert(0, container)
            container = container.parent
        return containers

    @property
    def level(self) -> int:
        level = 0
        
        item = self._item
        while item.parent and not isinstance(item.parent.obj, ModuleType):
            level += 1
            item = item.parent
        
        return level
    
    def _parse_itemname(self, name):
        description = self._parse_name(name)
        description = re.sub(
            r'^(test|describe)',
            'A',
            description)
        # description = re.sub(
        #     r'^(with)',
        #     'with',
        #     description)
        return description


class ItemFactory:
    def __init__(self) -> None:
        self.container_factory = ContainerFactory()

    def create(self, item: pytest.Item) -> Test:
        test_item = Test(item)

        container_item = item.parent
        container = self.container_factory.create(container_item)
        if container:
            container.add(test_item)       

        return test_item
        

class ContainerFactory:
    def __init__(self) -> None:
        self.containers: Dict[str, Container] = dict()

    def create(self, item) -> Container:
        containers = self._create_containers(item)
        if not containers:
            return None
        
        return containers[-1]
    
    def _create_unique_container(self, item):
        if item not in self.containers:
            container = Container(item)
            self.containers[item] = container

        container = self.containers.get(item)
        return container

    def _create_containers(self, item):
        containers = []
        child_container = None
        while item and not isinstance(item.obj, ModuleType):
            container = self._create_unique_container(item)
            if child_container:
                container.add_container(child_container)

            containers.insert(0, container)
            child_container = container
            item = item.parent
        return containers