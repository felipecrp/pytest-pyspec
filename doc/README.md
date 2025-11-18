# pytest-pyspec Documentation

Welcome to the **pytest-pyspec** documentation. This plugin transforms pytest output into a beautiful, readable format inspired by RSpec.

## Table of Contents

- [Installation](installation.md)
- [Getting Started](getting-started.md)
- [Naming Conventions](naming-conventions.md)
- [Using Docstrings](docstrings.md)
- [Advanced Features](advanced-features.md)
- [Examples](examples.md)
- [Configuration](configuration.md)

## Quick Links

- [GitHub Repository](https://github.com/felipecrp/pytest-pyspec)
- [PyPI Package](https://pypi.org/project/pytest-pyspec/)
- [Issue Tracker](https://github.com/felipecrp/pytest-pyspec/issues)

## Overview

**pytest-pyspec** enhances your testing workflow by making test output more readable and meaningful. Instead of seeing cryptic test paths and names, you'll see beautifully formatted, hierarchical descriptions of what your tests are doing.

### Key Benefits

- **Improved Readability**: Test output reads like documentation
- **Better Organization**: Clear hierarchical structure shows test relationships
- **Faster Debugging**: Quickly identify which tests failed and in what context
- **Team Communication**: Share test results that non-developers can understand
- **Living Documentation**: Tests serve as executable specifications

## What's New in v1.0.0

- **`when` prefix support**: Use `WhenTheUserIsLoggedIn` for temporal/conditional contexts
- **Lowercase formatting**: All prefixes (a/an, with/without, when) are now lowercase for consistency
- **Smart word capitalization**: Common words (the, is, are, etc.) are automatically lowercased in the middle of descriptions
- **Consolidated output**: Parent headers are shown only once, eliminating repetition
- **Enhanced readability**: Natural language output that's easier to read
- **Decorator helpers**: Override descriptions right beside your code

## Getting Help

If you need help or have questions:

1. Check the [documentation](README.md)
2. Look at the [examples](examples.md)
3. Search [existing issues](https://github.com/felipecrp/pytest-pyspec/issues)
4. Create a [new issue](https://github.com/felipecrp/pytest-pyspec/issues/new)

## Contributing

Contributions are welcome! Please see the project repository for contribution guidelines.

## License

MIT License - see the LICENSE file in the project repository.
