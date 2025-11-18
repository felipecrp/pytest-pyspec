# Changelog

All notable changes to this project are documented here. Release information is
derived from the Git history and tagged versions.

## [1.1.0] - Unreleased
- Introduced decorator helpers (`describe`, `with_`, `without`, `when`, `it`) so descriptions can be customized without relying on docstrings.

## [1.0.0]
- First stable release
- Established naming conventions for `Describe`/`Test` classes, `With`/`Without`/`When` contexts, and `test_`/`it_` functions.
- Docstrings can override any generated description, making the output read like documentation.
- Consolidated output formatting, expanded module/package reporting, and significantly improved tree building and CI coverage.
