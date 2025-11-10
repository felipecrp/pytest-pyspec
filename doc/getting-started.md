# Getting Started

## Basic Usage

Once you have pytest-pyspec installed, using it is simple. Just add the `--pyspec` flag when running pytest:

```bash
pytest --pyspec
```

## Your First Test

Create a simple test file `test_example.py`:

```python
class TestCalculator:
    def test_adds_numbers(self):
        assert 1 + 1 == 2
    
    def test_subtracts_numbers(self):
        assert 5 - 3 == 2
```

Run it with pytest-pyspec:

```bash
pytest test_example.py --pyspec
```

Output:

```
a Calculator
  ✓ adds numbers
  ✓ subtracts numbers
```

## Adding Context

You can organize related tests using context classes:

```python
class TestUser:
    class WithValidCredentials:
        def test_can_login(self):
            assert True
        
        def test_receives_auth_token(self):
            assert True
    
    class WithoutValidCredentials:
        def test_cannot_login(self):
            assert True
```

Output:

```
a User
  with Valid Credentials
    ✓ can login
    ✓ receives auth token

  without Valid Credentials
    ✓ cannot login
```

## Using the `when` Prefix

For temporal or conditional contexts, use the `when` prefix:

```python
class TestShoppingCart:
    class WhenTheCartIsEmpty:
        def test_shows_empty_message(self):
            assert True
    
    class WhenItemsAreAdded:
        def test_updates_total(self):
            assert True
        
        def test_shows_item_count(self):
            assert True
```

Output:

```
a Shopping Cart
  when the Cart is Empty
    ✓ shows empty message

  when Items are Added
    ✓ updates total
    ✓ shows item count
```

## Understanding the Output

### Status Symbols

- `✓` - Test passed
- `✗` - Test failed
- `»` - Test skipped

### Indentation

- **No indentation**: Test class (object being tested)
- **One level**: Context or direct test
- **Two+ levels**: Nested contexts and their tests

### Automatic Formatting

pytest-pyspec automatically:
- Converts CamelCase to readable text
- Lowercases common words (the, is, are, etc.) in the middle of descriptions
- Removes test-related prefixes (test, describe, it, with, without, when)
- Uses lowercase articles (a/an) for consistency

## Next Steps

- [Naming Conventions](naming-conventions.md) - Learn about all available prefixes
- [Using Docstrings](docstrings.md) - Customize test descriptions
- [Advanced Features](advanced-features.md) - Explore more capabilities
