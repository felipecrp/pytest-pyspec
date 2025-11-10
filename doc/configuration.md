# Configuration

## Basic Configuration

pytest-pyspec requires minimal configuration. Simply use the `--pyspec` flag:

```bash
pytest --pyspec
```

## Command Line Options

### `--pyspec`

Enables pytest-pyspec output formatting.

```bash
pytest --pyspec
```

### Combining with pytest Options

pytest-pyspec works with all standard pytest options:

```bash
# Run with coverage
pytest --pyspec --cov

# Run specific tests
pytest --pyspec test_auth.py

# Run with markers
pytest --pyspec -m "slow"

# Run with keyword filter
pytest --pyspec -k "authentication"

# Show detailed output (disables pyspec formatting)
pytest --pyspec -v  # Uses pytest's verbose mode instead
```

## Configuration File

### pytest.ini

You can set pyspec as the default in your `pytest.ini`:

```ini
[pytest]
addopts = --pyspec
```

Now you can just run:
```bash
pytest
```

### pyproject.toml

For projects using `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--pyspec"
```

### setup.cfg

For projects using `setup.cfg`:

```cfg
[tool:pytest]
addopts = --pyspec
```

## Disabling for Specific Runs

If you have pyspec enabled by default, you can disable it for a specific run:

```bash
# The -v flag disables pyspec formatting
pytest -v
```

## CI/CD Configuration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install pytest pytest-pyspec
      - name: Run tests
        run: pytest --pyspec
```

### GitLab CI

```yaml
test:
  image: python:3.11
  script:
    - pip install pytest pytest-pyspec
    - pytest --pyspec
```

### Travis CI

```yaml
language: python
python:
  - "3.10"
  - "3.11"
  - "3.12"
install:
  - pip install pytest pytest-pyspec
script:
  - pytest --pyspec
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest pytest-pyspec'
                sh 'pytest --pyspec'
            }
        }
    }
}
```

## Test Discovery Configuration

pytest-pyspec automatically extends pytest's test discovery to recognize:

- **Test classes**: `Test*`, `Describe*`, `With*`, `Without*`, `When*`
- **Test functions**: `test_*`, `it_*`

These are configured automatically when using `--pyspec`. No manual configuration needed!

## Advanced Configuration

### Custom Test Discovery Patterns

If you need to extend discovery further, you can modify pytest's configuration:

```ini
[pytest]
python_classes = Test* Describe* With* Without* When* MyCustomPrefix*
python_functions = test_* it_* my_custom_prefix_*
```

However, note that pytest-pyspec won't format custom prefixes automatically.

### Parallel Execution

pytest-pyspec works with pytest-xdist for parallel execution:

```bash
pip install pytest-xdist
pytest --pyspec -n auto
```

### Code Coverage

Works seamlessly with pytest-cov:

```bash
pip install pytest-cov
pytest --pyspec --cov=myproject --cov-report=html
```

## Performance Tuning

For large test suites:

### 1. Use Test Selection

Run only relevant tests:
```bash
pytest --pyspec test/unit/  # Only unit tests
pytest --pyspec -k "user"   # Only tests matching "user"
```

### 2. Parallel Execution

Use pytest-xdist:
```bash
pytest --pyspec -n 4  # Run on 4 cores
```

### 3. Disable Slow Features

For very large suites, consider running without pyspec in CI for faster execution, and use pyspec locally for development:

```yaml
# .github/workflows/tests.yml
- name: Run tests (fast)
  run: pytest  # No --pyspec flag for speed

- name: Run tests (formatted)
  if: github.event_name == 'pull_request'
  run: pytest --pyspec  # Use pyspec only for PRs
```

## Troubleshooting

### Tests Not Discovered

Make sure your test classes and functions use supported prefixes:
- Classes: `Test`, `Describe`, `With`, `Without`, `When`
- Functions: `test_`, `it_`

### Output Not Formatted

Check that:
1. You're using the `--pyspec` flag
2. You're not using `-v` (verbose mode disables pyspec)
3. pytest-pyspec is installed: `pip list | grep pytest-pyspec`

### Conflicts with Other Plugins

pytest-pyspec is designed to be compatible with other pytest plugins. If you experience conflicts:

1. Try running with only pyspec: `pytest --pyspec -p no:otherplugin`
2. Report the issue on [GitHub](https://github.com/felipecrp/pytest-pyspec/issues)

## Environment Variables

Currently, pytest-pyspec doesn't use environment variables for configuration. All configuration is done through command-line flags or pytest configuration files.

## Version Compatibility

- **Python**: 3.10+
- **pytest**: 9.0+

Check compatibility:
```bash
python --version
pytest --version
```

## Getting Help

For configuration issues:

1. Check the [documentation](README.md)
2. See [examples](examples.md)
3. Search [existing issues](https://github.com/felipecrp/pytest-pyspec/issues)
4. Create a [new issue](https://github.com/felipecrp/pytest-pyspec/issues/new)

## Next Steps

- [Examples](examples.md) - See real-world configurations
- [GitHub Repository](https://github.com/felipecrp/pytest-pyspec) - Source code and issues
