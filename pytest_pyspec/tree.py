"""
Semantic tree structure for pytest-pyspec.

Provides specific node types for different levels of test organization.
"""

from types import ModuleType
from typing import Dict, Optional
import re
import pytest


class PytestNode:
    """Base class for all semantic tree nodes."""
    
    # Subclasses can override these
    prefixes_to_remove = []
    description_prefix = None
    
    def __init__(self, item: pytest.Item):
        self._item = item
        # Store original name before any modifications
        self._original_name = item.name
    
    @property
    def description(self) -> str:
        """Return the base description without article/prefix."""
        docstring = getattr(self._item.obj, "__doc__", None)
        if docstring:
            first_line = docstring.splitlines()[0].strip()
            return first_line
        return self._description_from_identifier(self._original_name)
    
    @property
    def description_with_prefix(self) -> str:
        """Return the description with appropriate prefix (a/an, with/without)."""
        return self._apply_description_prefix(self.description)
    
    def _description_from_identifier(self, name: str) -> str:
        """Convert a Python identifier into a human-readable description."""
        normalized = self._convert_identifier_to_words(name)
        
        # Remove configured prefixes
        normalized = self._remove_test_prefixes(normalized)
        
        return normalized
    
    def _convert_identifier_to_words(self, name: str) -> str:
        """Convert Python identifier to words (CamelCase and snake_case)."""
        # First replace underscores with spaces
        name = name.replace('_', ' ')
        # Insert spaces before capitals (except at start)
        with_spaces = re.sub(r'(?!^)([A-Z])', r' \g<1>', name)
        # Normalize multiple spaces to single space
        with_spaces = ' '.join(with_spaces.split())
        return with_spaces
    
    def _remove_test_prefixes(self, text: str) -> str:
        """Remove configured test-related prefixes (test, describe, it, etc.)."""
        for prefix in self.prefixes_to_remove:
            pattern = rf'^{prefix}\s+'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text
    
    def _apply_description_prefix(self, text: str) -> str:
        """Add appropriate prefix (article or conjunction) to the description."""
        if not self.description_prefix:
            return text
        
        # Don't add prefix if already starts with with/without
        if text.lower().startswith(('with ', 'without ')):
            return text
        
        prefix = self._select_article_for_text(text)
        return f"{prefix} {text}"
    
    def _select_article_for_text(self, text: str) -> str:
        """Select appropriate article (a vs an) and match text capitalization."""
        if not self.description_prefix:
            return ""
        
        first_char = text[0].lower() if text else 'x'
        use_an = first_char in 'aeiou'
        
        if self.description_prefix.lower() == 'a':
            article = 'an' if use_an else 'a'
        else:
            article = self.description_prefix
        
        # Match capitalization of the text
        if text and text[0].isupper():
            article = article.capitalize()
        
        return article
    
    @property
    def level(self) -> int:
        """Calculate depth in the tree."""
        depth = 0
        node = self.parent if hasattr(self, 'parent') else None
        while node:
            depth += 1
            node = node.parent if hasattr(node, 'parent') else None
        return depth
    
    def format_for_output(self) -> str:
        """Format this node as a string for display output."""
        raise NotImplementedError("Subclasses must implement format_for_output()")


class TestFile(PytestNode):
    """Represents a test file (module)."""
    prefixes_to_remove = ['test']
    description_prefix = None
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.described_objects: list['DescribedObject'] = []
    
    def add_described_object(self, described_object: 'DescribedObject') -> None:
        """Add a top-level test class to this file."""
        self.described_objects.append(described_object)
        described_object.parent = self
    
    def format_for_output(self) -> str:
        """Format test file for display output."""
        indent = "  " * self.level
        return f"{indent}{self.description_with_prefix}"


class DescribedObject(PytestNode):
    """Represents a top-level test class (e.g., DescribeMyClass)."""
    prefixes_to_remove = ['test', 'describe']
    description_prefix = 'a'
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.parent: Optional[TestFile] = None
        self.contexts: list['TestContext'] = []
        self.tests: list['Test'] = []
    
    def add_context(self, context: 'TestContext') -> None:
        """Add a nested context to this described object."""
        self.contexts.append(context)
        context.parent = self
    
    def add_test(self, test: 'Test') -> None:
        """Add a test directly to this described object."""
        self.tests.append(test)
        test.parent = self
    
    def format_for_output(self) -> str:
        """Format described object for display output."""
        indent = "  " * self.level
        return f"{indent}{self.description_with_prefix}"


class TestContext(PytestNode):
    """Represents a nested context class (e.g., WithSomeCondition)."""
    prefixes_to_remove = ['test']
    description_prefix = None
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.parent: Optional['DescribedObject | TestContext'] = None
        self.contexts: list['TestContext'] = []
        self.tests: list['Test'] = []
    
    def add_context(self, context: 'TestContext') -> None:
        """Add a nested context to this context."""
        self.contexts.append(context)
        context.parent = self
    
    def add_test(self, test: 'Test') -> None:
        """Add a test to this context."""
        self.tests.append(test)
        test.parent = self
    
    def _apply_description_prefix(self, text: str) -> str:
        """For contexts, ensure 'with'/'without' are lowercase."""
        if text.lower().startswith('with '):
            return 'with' + text[4:]
        elif text.lower().startswith('without '):
            return 'without' + text[7:]
        return text
    
    def format_for_output(self) -> str:
        """Format context for display output."""
        indent = "  " * self.level
        return f"{indent}{self.description_with_prefix}"


class Test(PytestNode):
    """Represents an individual test function."""
    prefixes_to_remove = ['test', 'it']
    description_prefix = None
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.parent: Optional['DescribedObject | TestContext'] = None
        self.outcome: Optional[str] = None
    
    def format_for_output(self) -> str:
        """Format test for display output with status symbol."""
        indent = "  " * self.level
        status = self._get_status_symbol()
        return f"{indent}{status} {self.description}"
    
    def _get_status_symbol(self) -> str:
        """Get the status symbol based on test outcome."""
        if self.outcome == 'passed':
            return '✓'
        elif self.outcome == 'failed':
            return '✗'
        else:
            return '»'
    
    def get_parent_tree_string(self) -> str:
        """Get formatted string of all parent nodes from root to this test."""
        output = ""
        if self.parent:
            # Collect parent nodes
            nodes = []
            current = self.parent
            while current:
                # Skip TestFile nodes as they're not typically displayed
                if not isinstance(current, TestFile):
                    nodes.insert(0, current)
                current = current.parent if hasattr(current, 'parent') else None
            
            # Convert each parent node to string
            for node in nodes:
                output += "\n" + node.format_for_output()
        return output


class SemanticTreeBuilder:
    """Factory for building the semantic tree from pytest items."""
    
    def __init__(self):
        self._node_cache: Dict[pytest.Item, PytestNode] = {}
    
    def build_tree_for_test(self, test_item: pytest.Item) -> Test:
        """Build a Test node and its complete ancestor tree."""
        test = Test(test_item)
        self._node_cache[test_item] = test
        
        # Build the parent chain from bottom to top
        child_node = test
        parent_item = test_item.parent
        
        while parent_item and not isinstance(parent_item.obj, ModuleType):
            if parent_item in self._node_cache:
                parent_node = self._node_cache[parent_item]
            else:
                parent_node = self._create_node(parent_item)
                self._node_cache[parent_item] = parent_node
            
            # Link child to parent using type-specific methods
            if not hasattr(child_node, 'parent') or child_node.parent is None:
                self._link_child_to_parent(parent_node, child_node)
            
            # Move up the tree
            child_node = parent_node
            parent_item = parent_item.parent
        
        return test
    
    def _link_child_to_parent(self, parent: PytestNode, child: PytestNode) -> None:
        """Link a child node to its parent using type-specific methods."""
        if isinstance(child, Test):
            if isinstance(parent, (DescribedObject, TestContext)):
                parent.add_test(child)
        elif isinstance(child, TestContext):
            if isinstance(parent, DescribedObject):
                parent.add_context(child)
            elif isinstance(parent, TestContext):
                parent.add_context(child)
        elif isinstance(child, DescribedObject):
            if isinstance(parent, TestFile):
                parent.add_described_object(child)
    
    def _create_node(self, item: pytest.Item) -> PytestNode:
        """Create the appropriate node type based on item characteristics."""
        if hasattr(item, 'parent') and item.parent:
            parent_obj = item.parent.obj
            
            if isinstance(parent_obj, ModuleType):
                return DescribedObject(item)
            
            return TestContext(item)
        
        return DescribedObject(item)
    
    def get_root_node(self, test: Test) -> Optional[PytestNode]:
        """Get the root node."""
        node = test
        while node.parent:
            node = node.parent
        return node if node != test else None
