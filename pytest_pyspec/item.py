from types import ModuleType
import pytest

class Item:
    def __init__(self, item: pytest.Item) -> None:
        self._item = item

    @property
    def description(self):        
        description = self._item.obj.__doc__

        if not description:
            description = self._item.name
            description = self._parse_description(description)

        description = description.splitlines()[0]
        description = description.capitalize()
        return description

    def _parse_description(self, description: str):
        split = False
        if description.lower().startswith("it_"):
            description = description.replace('it_', '')
            split = True

        if description.lower().startswith("test_it_"):
            description = description.replace('test_it_', '')
            split = True

        if description.lower().startswith("test_describe_"):
            description = description.replace('test_describe_', '')
            split = True

        if description.lower().startswith("describe_"):
            description = description.replace('describe_', '')
            split = True

        if split:
            description = description.replace('_', ' ')

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
        return self.container.level +1
   
    
class Container(Item):
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.tests = list[Test]()
        self.containers = list[Container]()
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


class ItemFactory:
    def __init__(self) -> None:
        self.container_factory = ContainerFactory()

    def create(self, item: pytest.Item) -> Test:
        test_item = Test(item)

        container_item = item.parent
        container = self.container_factory.create(container_item)
        container.add(test_item)       

        return test_item
        

class ContainerFactory:
    def __init__(self) -> None:
        self.containers = dict[str, Container]()

    def create(self, item) -> Container:
        containers = self._create_containers(item)
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