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

        description = description.splitlines()[0]
        description = description.capitalize()
        return description


class Test(Item):
    def __init__(self, item: pytest.Item) -> None:
        super().__init__(item)
        self.container: Container = None
   
    
class Container(Item):
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.tests = list[Test]()

    def add(self, test: Test):
        self.tests.append(test)
        test.container = self


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
        if item not in self.containers:
            container = Container(item)
            self.containers[item] = container

        container = self.containers.get(item)
        return container
