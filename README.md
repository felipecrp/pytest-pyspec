[![](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml/badge.svg)](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml)

# pytest-pyspec

The **pytest-pyspec** plugin transforms pytest output into a beautiful, readable format similar to RSpec. It provides semantic meaning to your tests by organizing them into descriptive hierarchies, using the prefixes `Describe`/`Test`, `With`/`Without`/`When`, and `test_`/`it_`, while allowing docstrings and decorators to override the descriptions.

## Features

- **Semantic Output**: Transform pytest's default output into readable, hierarchical descriptions
- **Multiple Prefixes**: Support for `describe/test` (objects), `with/without/when` (contexts), and `it/test` (tests)
- **Docstring Support**: Override test descriptions using docstrings
- **Consolidated Output**: Smart grouping that avoids repeating parent headers
- **Natural Language**: Automatic lowercase formatting of common words (the, is, are, etc.)
- **Decorator Support**: Override descriptions right next to your classes and tests

## Quick Start

### Installation

```bash
pip install pytest pytest-pyspec
```

### Running

```bash
pytest --pyspec
```

## Examples

### Car Scenario

A minimal car example with properties and behaviors:

```python
class DescribeCar:
    def test_has_engine(self):
        assert True

    class WithFullTank:
        def test_drive_long_distance(self):
            assert True

    class WithoutFuel:
        def test_cannot_start_engine(self):
            assert True

    class WhenTheEngineIsRunning:
        def test_consumes_fuel(self):
            assert True
```

With **pytest-pyspec**, this produces:

```
a Car
  ✓ has engine

  with Full Tank
    ✓ drive long distance

  without Fuel
    ✓ cannot start engine

  when the Engine is Running
    ✓ consumes fuel
```

### Available Prefixes

**pytest-pyspec** supports three types of prefixes to create semantic test hierarchies:

#### 1. Object Classes (use `describe` or `test`)

Define what you're testing:

```python
class DescribeCar:  # or class TestCar:
    def test_has_four_wheels(self):
        assert True
```

Output:
```
a Car
  ✓ has four wheels
```

#### 2. Context Classes (use `with`, `without`, or `when`)

Define the context or state:

```python
class DescribeCar:
    class WithFullTank:
        def test_can_drive_long_distances(self):
            assert True

    class WithoutFuel:
        def test_cannot_start_engine(self):
            assert True

    class WhenTheEngineIsRunning:
        def test_consumes_fuel(self):
            assert True
```

Output:
```
a Car
  with Full Tank
    ✓ can drive long distances

  without Fuel
    ✓ cannot start engine

  when the Engine is Running
    ✓ consumes fuel
```

#### 3. Test Functions (use `it_` or `test_`)

Define the expected behavior:

```python
class DescribeCar:
    def it_has_four_wheels(self):
        assert True

    def test_has_engine(self):
        assert True
```

Output:
```
a Car
  ✓ has four wheels
  ✓ has engine
```

### Using Docstrings

Override automatic naming with custom descriptions:

```python
class TestCar:
    """sports car"""
    
    def test_top_speed(self):
        """reaches 200 mph"""
        assert True

    class WhenTheNitroIsActivated:
        """when nitro boost is activated"""
        
        def test_acceleration(self):
            """accelerates rapidly"""
            assert True
```

Output:
```
a sports car
  ✓ reaches 200 mph

  when nitro boost is activated
    ✓ accelerates rapidly
```

### Using Decorators

Prefer decorators over docstrings? Import the helpers directly from `pytest_pyspec`:

```python
import pytest_pyspec as spec

@spec.describe("Car")
class DescribeCar:
    @spec.it("reaches 200 mph")
    def test_top_speed(self):
        assert True

    @spec.when("nitro boost is activated")
    class WhenTheNitroIsActivated:
        @spec.it("accelerates rapidly")
        def test_acceleration(self):
            assert True
```

Output:
```
a Car
  ✓ reaches 200 mph

  when nitro boost is activated
    ✓ accelerates rapidly
```

You can also import individual helpers (`describe`, `with_`, `without`, `when`,
`it`) directly from `pytest_pyspec` if you prefer `from ... import ...` style.
`with` is still exposed as `with_` because the plain name is reserved.

Decorators always win when both a docstring and a decorator are present, so you
can keep docstrings for documentation/IDE help while letting decorators drive
runtime output.

## Configuration

The plugin is automatically enabled when you use the `--pyspec` flag. No additional configuration is required.

For more information, see the [documentation](https://github.com/felipecrp/pytest-pyspec/blob/main/doc/README.md).
