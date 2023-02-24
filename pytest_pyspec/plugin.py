from os import wait
import time
from typing import List, Sequence, Union

import pytest
import _pytest
from _pytest.terminal import TerminalReporter

def pytest_addoption(parser: pytest.Parser, 
                     pluginmanager: pytest.PytestPluginManager):
    group = parser.getgroup('general')
    group.addoption(
        '--pyspec',
        action='store_true',
        dest='pyspec',
        help='Enables pyspec features'
    )

enabled = False
def pytest_configure(config: pytest.Config):
    global enabled
    if config.getoption('pyspec') and not config.getoption('verbose'):
        enabled = True

def node_to_list(node):
    current_node = node
    nodes = [current_node]
    while current_node.parent:
        current_node = current_node.parent
        nodes.insert(0, current_node)
    return nodes


class TestItem:
    def __init__(self, item, previous_test_item):
        self._item = item
        self._previous_test_item = previous_test_item
        self._nodes = node_to_list(item)

    def level(self):
        return len(self._nodes)
    
    def parent(self, level):
        return self._nodes[level]
    
    def _get_identation(self):
        return ' '.join([' ']*self.level())
    
    def format_setup(self):
        test_mark = ' '
        
        depth = self._calculate_depth()
        output = self.output(depth)
        return '', output, (output, {"white": True})

    def format_teardown(self):
        return ('', '\n', '')
    
    def name(self):
        return self._item.name
    
    def _calculate_depth(self) -> int:
        if not self._previous_test_item:
            return self.level()
        
        if self._item.parent != self._previous_test_item._item.parent:
            return self.level()
        
        depth = self.level() - self._previous_test_item.level()

        if depth == 0:
            depth += 1
        return depth

    def output(self, depth: int) -> str:
        output = ''
        show_output = len(self._nodes) - 2 - depth
        last_line = self.level() - 3
        for i, node in enumerate(self._nodes[2:]):
            ident = '  ' * (i)
            if i >= show_output:
                line = f"\n  {ident}{self._get_name(node)}"
                if i == last_line:
                    line = f"{line:70}"
                output += line
        # output += '\r'
        return output
    
    def _get_name(self, node):
        name: str = node.obj.__doc__
        if name:
            name = name.splitlines()[0]
        if not name:
            name = node.name
        name = name.capitalize()
        return name

test_item_key = pytest.StashKey[TestItem]()
def pytest_collection_modifyitems(session, config, items):
    previous_test_item = None
    for i, item in enumerate(items):
        test_item = TestItem(item, previous_test_item)
        item.stash[test_item_key] = test_item
        previous_test_item = test_item


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report: pytest.Report = outcome.get_result()
    report.item = item


def pytest_report_teststatus(report: pytest.TestReport, config: pytest.Config):
    if enabled:
        item = report.item
        test_item = item.stash[test_item_key]
        
        if report.when == 'setup':
            return test_item.format_setup()
    
    # if report.when == 'call':
    #     if report.passed:
    #         return ('passed', '.\n', ('passed', {'green': True}))
    
    # if report.when == 'teardown':
    #     return test_item.format_teardown()
