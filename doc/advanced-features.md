# Advanced Features

## Consolidated Output

One of the most powerful features of pytest-pyspec is **consolidated output**, which eliminates repetition by showing parent headers only once.

```python
class TestUser:
    def test_has_email(self):
        assert True
    
    def test_has_password(self):
        assert True
    
    def test_can_authenticate(self):
        assert True
```

Produces:
```
a User
  ✓ has email
  ✓ has password
  ✓ can authenticate
```

The parent header appears only once, making the output much cleaner!

## Smart Word Capitalization

pytest-pyspec automatically lowercases common words in the middle of descriptions:

### Common Words List

These words are automatically lowercased (except at the start):
- **Articles**: the, a, an
- **Conjunctions**: and, or, but, nor, for, yet, so
- **Auxiliary verbs**: is, are, was, were, be, been, being, has, have, had, do, does, did
- **Prepositions**: in, on, at, to, of, by, with, from, as

### Examples

```python
class WhenTheUserIsLoggedIn:
    pass
```
Output: `when the User is Logged In`

```python
class WithTheFeatureEnabled:
    pass
```
Output: `with the Feature Enabled`

```python
class TestAPIController:
    pass
```
Output: `an API Controller` (leading vowel uses "an")

## Nested Contexts

You can create deeply nested test hierarchies:

```python
class DescribeOnlineStore:
    class WithAuthenticatedUser:
        class WhenTheCartHasItems:
            class WithValidCouponCode:
                def test_applies_discount(self):
                    assert True
```

Output:
```
an Online Store
  with Authenticated User
    when the Cart Has Items
      with Valid Coupon Code
        ✓ applies discount
```

## Organizing Large Test Suites

### Strategy 1: Group by Feature

```python
# test_authentication.py
class DescribeAuthentication:
    class WhenLoggingIn:
        pass
    
    class WhenLoggingOut:
        pass
    
    class WhenResettingPassword:
        pass

# test_shopping.py
class DescribeShoppingCart:
    pass

class DescribeCheckout:
    pass
```

### Strategy 2: Group by User Journey

```python
class DescribeUserRegistration:
    class WithValidEmail:
        pass
    
    class WithInvalidEmail:
        pass
    
    class WhenTheEmailIsAlreadyTaken:
        pass
```

### Strategy 3: Group by Component

```python
class DescribeDatabaseLayer:
    class WithPostgresConnection:
        pass
    
    class WithoutConnection:
        pass

class DescribeAPILayer:
    pass

class DescribeBusinessLogic:
    pass
```

## Running Specific Tests

Since pytest-pyspec works with standard pytest, all pytest features work:

### Run Specific Test Class

```bash
pytest test_file.py::TestUser --pyspec
```

### Run Specific Test

```bash
pytest test_file.py::TestUser::test_has_email --pyspec
```

### Run Tests Matching Pattern

```bash
pytest -k "authentication" --pyspec
```

### Run Tests by Marker

```python
import pytest

class DescribePayment:
    @pytest.mark.slow
    def test_processes_large_batch(self):
        assert True
```

```bash
pytest -m slow --pyspec
```

## Combining with pytest Fixtures

pytest-pyspec works seamlessly with fixtures:

```python
import pytest

@pytest.fixture
def user():
    return {"name": "John", "email": "john@example.com"}

class DescribeUser:
    def test_has_valid_email(self, user):
        assert "@" in user["email"]
    
    class WhenTheUserIsActive:
        def test_can_login(self, user):
            assert user is not None
```

## Parameterized Tests

Works great with `pytest.mark.parametrize`:

```python
import pytest

class DescribeCalculator:
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (5, 3, 8),
        (10, -5, 5)
    ])
    def test_adds_numbers(self, a, b, expected):
        assert a + b == expected
```

Output shows each parameterized test:
```
a Calculator
  ✓ adds numbers[1-2-3]
  ✓ adds numbers[5-3-8]
  ✓ adds numbers[10--5-5]
```

## Test Discovery

pytest-pyspec extends pytest's test discovery to recognize:

- **Classes starting with**: `Test`, `Describe`, `With`, `Without`, `When`
- **Functions starting with**: `test_`, `it_`

All are discovered automatically when you run pytest with the `--pyspec` flag.

## Performance Considerations

pytest-pyspec adds minimal overhead to test execution:

- **Output formatting**: Only runs when tests complete (no impact on test execution time)
- **Tree building**: Efficient caching prevents redundant processing
- **Memory usage**: Minimal - only stores test metadata

For large test suites (1000+ tests), the performance impact is negligible (< 1% overhead).

## Compatibility

pytest-pyspec is compatible with:

- ✅ pytest plugins (pytest-cov, pytest-xdist, etc.)
- ✅ pytest fixtures
- ✅ pytest markers
- ✅ pytest parametrize
- ✅ pytest hooks
- ✅ All major CI/CD systems

## Verbose Mode

When using pytest's verbose mode (`-v`), pytest-pyspec automatically defers to pytest's default output to avoid conflicts:

```bash
pytest --pyspec -v  # Uses pytest's default verbose output
pytest --pyspec     # Uses pyspec formatted output
```

## Decorator Helpers

Prefer decorating classes functions instead of relying on naming/docstrings?
Import helpers from `pytest_pyspec`:

```python
import pytest_pyspec as spec

@spec.describe("API client")
class DescribeClient:
    @spec.with_("valid credentials")
    class WithValidCredentials:
        @spec.it("authenticates successfully")
        def test_auth(self):
            assert True
```

Decorators can be mixed with docstrings and always override them when both are
present, letting you keep docstrings for IDEs while still controlling output.

## Next Steps

- [Examples](examples.md) - See complete real-world examples
- [Configuration](configuration.md) - Learn about configuration options
