
"""
Pytest plugin that prints test output in an RSpec-like, readable format.

When enabled with the ``--pyspec`` flag, this plugin:
  - Extends test discovery to also match ``it_`` functions and classes whose
    names start with ``Describe``, ``With``, ``Without``, or ``When``.
  - Builds a tree of containers/tests and renders them with friendly
    descriptions (favoring docstrings when present).
  - Uses pytest's stash to pass the current/previous Test objects between
    hooks, so we can decide when to print a container header.
"""
from typing import Any, Tuple, Generator

import pytest
from pytest_pyspec.tree import SemanticTreeBuilder, Test


def pytest_addoption(
    parser: pytest.Parser,
    pluginmanager: pytest.PytestPluginManager
) -> None:
    """
    Register the ``--pyspec`` command-line flag.

    The flag toggles all formatting and discovery behavior provided by this
    plugin. We keep discovery changes behind the flag to avoid surprises in
    normal pytest runs.
    """
    group = parser.getgroup('general')
    group.addoption(
        '--pyspec',
        action='store_true',
        dest='pyspec',
        help='Enables pyspec features'
    )


ENABLED_KEY = pytest.StashKey[bool]()
def pytest_configure(config: pytest.Config) -> None:
    """
    Initialize plugin state and, when enabled, extend test discovery rules.

    - ``enabled`` is set only when ``--pyspec`` is present and ``-v`` is not
      used (verbose mode already prints enough, so we defer to pytest's
      default output in that case).
    - Appends discovery patterns for ``it_`` functions and ``Describe``, ``With``,
      ``Without``, and ``When`` classes when pyspec is on.
    """
    # Store enabled state in config.stash for access in all hooks.
    enabled = config.getoption('pyspec') and not config.getoption('verbose')
    config.stash[ENABLED_KEY] = enabled

    if config.getoption('pyspec'):
        # Extend discovery to match RSpec-like naming.
        python_functions = config.getini("python_functions")
        python_functions.append('it_')
        config.option.python_functions = python_functions

        python_classes = config.getini("python_classes")
        python_classes.append('Describe')
        python_classes.append('With')
        python_classes.append('Without')
        python_classes.append('When')
        config.option.python_classes = python_classes


# Stash keys used to share Test objects between hooks.
# These allow the report hook to know the current and previous test, so we can
# decide when to print a container header (on container change).
TEST_KEY = pytest.StashKey[Test]()
PREV_TEST_KEY = pytest.StashKey[Test]()
def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """
    After collection, wrap each pytest item with our Test model and stash it.

    The previous Test is also stashed so later hooks can determine container
    boundaries and print headers only when the container changes.
    """
    enabled = config.stash.get(ENABLED_KEY, False)
    if enabled:
        builder = SemanticTreeBuilder()
        prev_test = None
        processed_parents = set()
        
        for i, item in enumerate(items):
            test = builder.build_tree_for_test(item)
            item.stash[TEST_KEY] = test
            item.stash[PREV_TEST_KEY] = prev_test
            prev_test = test
            
            # Update item name to the test case description with prefix for VSCode
            item.name = test.description_with_prefix
            
            # Update parent node names for VSCode test explorer (only once per parent)
            current = test.parent
            while current is not None and hasattr(current, '_item'):
                if current._item not in processed_parents:
                    current._item.name = current.description_with_prefix
                    processed_parents.add(current._item)
                current = current.parent if hasattr(current, 'parent') else None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo
) -> Generator[Any, Any, None]:
    """
    Inject Test metadata into the report object for later formatting.

    As a hookwrapper we yield to let pytest create the report, then attach our
    Test and prev_test (from stash) so ``pytest_report_teststatus`` can render
    the right lines.
    """
    outcome = yield
    enabled = item.config.stash.get(ENABLED_KEY, False)
    if enabled:
        report: pytest.Report = outcome.get_result()
        # TODO Check whether the report has a stash
        # TODO move previous test to test class
        if TEST_KEY in item.stash:
            report.test = item.stash[TEST_KEY]
            report.prev_test = item.stash[PREV_TEST_KEY]



def pytest_report_teststatus(
    report: pytest.TestReport,
    config: pytest.Config
) -> Any:
    """
    Produce short status and a human-friendly text line for each test event.

    Behavior (only when pyspec is enabled and a Test is attached):
    - On setup: if the parent nodes changed, print the parent tree.
    - On call (or skipped during setup): print the test line with its status
      mark. We reuse pytest's status tuple format.
    """
    enabled = config.stash.get(ENABLED_KEY, False)
    if enabled and hasattr(report, 'test'):
        test = report.test
        prev_test = report.prev_test

        if report.when == 'setup':
            # Check if we need to print parent nodes
            if not prev_test or test.parent != prev_test.parent:
                # Show only new parent nodes (not already displayed)
                output = test.get_new_parent_nodes_string(prev_test)
                return '', output, ('', {'white': True})

        # Determine if this is the last test with the same parent
        is_last_in_parent = False
        if test.parent and hasattr(test.parent, 'tests'):
            try:
                idx = test.parent.tests.index(test)
                is_last_in_parent = idx == len(test.parent.tests) - 1
            except (ValueError, AttributeError):
                pass

        if report.when == 'call':
            test.outcome = report.outcome
            output = test.format_for_output()
            # Always start test line with a newline
            output = '\n' + output
            # Only add a single newline after the last test in a parent
            if is_last_in_parent:
                output += '\n'
            return report.outcome, output, ''

        if report.when == 'setup' and report.skipped:
            test.outcome = report.outcome
            output = test.format_for_output()
            output = '\n' + output
            if is_last_in_parent:
                output += '\n'
            return report.outcome, output, ''