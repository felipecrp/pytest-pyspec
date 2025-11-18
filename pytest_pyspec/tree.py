"""
Semantic tree structure for pytest-pyspec.

Provides specific node types for different levels of test organization.
"""

from types import ModuleType
from typing import Dict, Optional
import re
import pytest
from pytest_pyspec.decorators import DESCRIPTION_ATTR


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
        decorator_desc = self._description_from_decorator()
        if decorator_desc:
            return decorator_desc
        docstring = self._description_from_docstring()
        if docstring:
            return docstring
        return self._description_from_identifier()
    
    @property
    def description_with_prefix(self) -> str:
        """Return the description with appropriate prefix (a/an, with/without/when)."""
        if not self.description_prefix:
            return self.description
        
        # For all prefixes, keep them lowercase
        return f"{self.description_prefix} {self.description}"

    def _description_from_decorator(self) -> Optional[str]:
        """Extract description stored by pyspec decorators."""
        return getattr(self._item.obj, DESCRIPTION_ATTR, None)
    
    def _description_from_docstring(self) -> Optional[str]:
        """Extract description from docstring if available."""
        docstring = getattr(self._item.obj, "__doc__", None)
        if docstring:
            first_line = docstring.splitlines()[0].strip()
            return first_line
        return None
    
    def _description_from_identifier(self) -> str:
        """Convert a Python identifier into a human-readable description."""
        # First convert identifier to words (CamelCase and snake_case)
        normalized = self._convert_identifier_to_words(self._original_name)
        # Lowercase common words (before removing prefixes to preserve proper casing)
        normalized = self._lowercase_common_words(normalized)
        # Then remove configured prefixes
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
    
    def _lowercase_common_words(self, text: str) -> str:
        """Lowercase common words (articles, prepositions, conjunctions) except at the start."""
        # Common words to lowercase (articles, prepositions, conjunctions, auxiliary verbs)
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'nor', 'for', 'yet', 'so',
            'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'has', 'have', 'had', 'do', 'does', 'did',
            'in', 'on', 'at', 'to', 'of', 'by', 'with', 'from', 'as'
        }
        
        words = text.split()
        if not words:
            return text
        
        # Keep the first word as-is, lowercase common words in the rest
        result = [words[0]]
        for word in words[1:]:
            if word.lower() in common_words:
                result.append(word.lower())
            else:
                result.append(word)
        
        return ' '.join(result)
    
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
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.parent: Optional[TestFile] = None
        self.contexts: list['TestContext'] = []
        self.tests: list['Test'] = []
    
    @property
    def description_prefix(self) -> str:
        """Return 'a' or 'an' based on the first letter of description."""
        first_char = self.description[0].lower() if self.description else 'x'
        return 'an' if first_char in 'aeiou' else 'a'
    
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
    prefixes_to_remove = ['test', 'with', 'without', 'when']
    
    def __init__(self, item: pytest.Item):
        super().__init__(item)
        self.parent: Optional['DescribedObject | TestContext'] = None
        self.contexts: list['TestContext'] = []
        self.tests: list['Test'] = []
    
    @property
    def description_prefix(self) -> Optional[str]:
        """Return 'with', 'without', or 'when' based on the original name."""
        name_lower = self._original_name.lower()
        # Check 'without' first since it contains 'with'
        if name_lower.startswith('without'):
            return 'without'
        # Check for 'when' prefix
        if name_lower.startswith('when'):
            return 'when'
        # All other contexts get 'with' prefix (including those starting with 'with')
        return 'with'
    
    @property
    def description_with_prefix(self) -> str:
        """Return description with prefix, keeping 'with'/'without'/'when' lowercase."""
        if not self.description_prefix:
            return self.description
        
        # Check if description already starts with the prefix
        desc_lower = self.description.lower()
        if desc_lower.startswith(f"{self.description_prefix} ") or desc_lower == self.description_prefix:
            # Description already has the prefix, return as-is
            return self.description
        
        # For contexts, always keep with/without/when lowercase
        return f"{self.description_prefix} {self.description}"
    
    def add_context(self, context: 'TestContext') -> None:
        """Add a nested context to this context."""
        self.contexts.append(context)
        context.parent = self
    
    def add_test(self, test: 'Test') -> None:
        """Add a test to this context."""
        self.tests.append(test)
        test.parent = self
    
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
        """Get formatted string of all parent nodes from root to this test.
        
        Builds the hierarchical header showing all parent contexts for a test.
        Called when the parent context changes between tests to display the
        full context path (e.g., "A Function" -> "with Test Case" -> "with Context").
        
        Returns:
            Multi-line string with formatted parent nodes, each on a new line.
            Skips TestFile nodes (module level) as they're not typically displayed.
            Returns empty string if test has no parents.
        """
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
    
    def get_new_parent_nodes_string(self, prev_test: Optional['Test']) -> str:
        """Get formatted string of only the new parent nodes since prev_test.
        
        Finds the common ancestor between this test and prev_test, then returns
        only the parent nodes that are new (not shared with prev_test).
        
        Args:
            prev_test: The previous test that was displayed
            
        Returns:
            Multi-line string with formatted new parent nodes, each on a new line.
            Returns empty string if no new parents need to be displayed.
        """
        if not prev_test:
            # No previous test, show all parents
            return self.get_parent_tree_string()
        
        # Get all parent nodes for both tests
        self_parents = []
        current = self.parent
        while current:
            if not isinstance(current, TestFile):
                self_parents.insert(0, current)
            current = current.parent if hasattr(current, 'parent') else None
        
        prev_parents = []
        current = prev_test.parent
        while current:
            if not isinstance(current, TestFile):
                prev_parents.insert(0, current)
            current = current.parent if hasattr(current, 'parent') else None
        
        # Find where the parent chains diverge
        common_depth = 0
        for i in range(min(len(self_parents), len(prev_parents))):
            if self_parents[i] is prev_parents[i]:
                common_depth = i + 1
            else:
                break
        
        # Only print the new parent nodes
        new_parents = self_parents[common_depth:]
        output = ""
        for node in new_parents:
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
