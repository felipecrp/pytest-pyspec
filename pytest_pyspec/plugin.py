import pytest
from pytest_pyspec.item import ItemFactory, Test
from pytest_pyspec.output import print_container, print_test


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

        python_functions = config.getini("python_functions")
        python_functions.append('it_')
        config.option.python_functions = python_functions

        python_classes = config.getini("python_classes")
        python_classes.append('Describe')
        python_classes.append('With')
        config.option.python_classes = python_classes


test_key = pytest.StashKey[Test]()
prev_test_key = pytest.StashKey[Test]()
def pytest_collection_modifyitems(session, config, items):
   if enabled:
        factory = ItemFactory()
        prev_test = None
        for i, item in enumerate(items):
            test = factory.create(item)
            item.stash[test_key] = test
            item.stash[prev_test_key] = prev_test
            prev_test = test


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if enabled:
        report: pytest.Report = outcome.get_result()
        #TODO Check whether the report has a stash
        #TODO move previous test to test class
        report.test = item.stash[test_key]
        report.prev_test = item.stash[prev_test_key]


def pytest_report_teststatus(report: pytest.TestReport, config: pytest.Config):
    if enabled:
        test = report.test
        prev_test = report.prev_test

        if report.when == 'setup':
            if not prev_test \
                    or test.container != prev_test.container:
                # Show container
                output = print_container(test.container)
                return '', output, ('', {'white': True})

        if report.when == 'call':
            test.outcome = report.outcome
            output = print_test(test)
            return report.outcome, output, ''
        
        if report.when == 'setup' and report.skipped:
            test.outcome = report.outcome
            output = print_test(test)
            return report.outcome, output, ''
        