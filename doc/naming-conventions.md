# Naming Conventions

**pytest-pyspec** uses specific naming prefixes to give semantic meaning to your tests. Understanding these conventions will help you write more expressive and readable tests.

## Class Prefixes

### Object Classes: `Test` or `Describe`

Use these prefixes to represent the object or feature being tested.

**Examples:**

```python
class TestUser:
    pass

class DescribePaymentProcessor:
    pass
```

**Output:**
```
a User
a Payment Processor
```

### Context Classes: `With`, `Without`, or `When`

Use these prefixes to represent different contexts or scenarios.

#### `With` - Presence of something

```python
class TestDatabase:
    class WithValidConnection:
        def test_can_query_data(self):
            assert True
```

**Output:**
```
a Database
  with Valid Connection
    ✓ can query data
```

#### `Without` - Absence of something

```python
class TestAPI:
    class WithoutAuthentication:
        def test_returns_401(self):
            assert True
```

**Output:**
```
an API
  without Authentication
    ✓ returns 401
```

#### `When` - Temporal or conditional scenarios

```python
class TestOrder:
    class WhenTheOrderIsShipped:
        def test_sends_notification(self):
            assert True
```

**Output:**
```
an Order
  when the Order is Shipped
    ✓ sends notification
```

## Function Prefixes

### Test Functions: `test_` or `it_`

Use these prefixes for individual test cases.

**Examples:**

```python
class DescribeCalculator:
    def test_adds_numbers(self):
        assert 1 + 1 == 2
    
    def it_divides_numbers(self):
        assert 10 / 2 == 5
```

**Output:**
```
a Calculator
  ✓ adds numbers
  ✓ divides numbers
```

## Naming Best Practices

### 1. Use Descriptive Names

❌ **Bad:**
```python
class TestUser:
    def test_a(self):
        pass
```

✅ **Good:**
```python
class TestUser:
    def test_can_update_profile(self):
        pass
```

### 2. Use CamelCase for Readability

The plugin automatically converts CamelCase to readable text:

```python
class WhenTheUserIsLoggedIn:
    pass
```

Output: `when the User is Logged In`

### 3. Be Specific with Contexts

❌ **Less Clear:**
```python
class WithData:
    pass
```

✅ **More Clear:**
```python
class WithValidUserData:
    pass
```

### 4. Use Natural Language

Think about how you would describe the test in conversation:

```python
class DescribeShoppingCart:
    class WhenTheCartHasThreeItems:
        def it_calculates_the_correct_total(self):
            pass
```

Output:
```
a Shopping Cart
  when the Cart Has Three Items
    ✓ calculates the correct total
```

## Automatic Transformations

pytest-pyspec automatically applies these transformations:

### 1. Prefix Removal

All standard prefixes are removed:
- `Test`, `Describe` → removed
- `With`, `Without`, `When` → removed (but reapplied as lowercase)
- `test_`, `it_` → removed

### 2. CamelCase Conversion

CamelCase is converted to separate words:
- `TestUserProfile` → `User Profile`
- `WhenTheUserLogsIn` → `the User Logs In`

### 3. Lowercase Common Words

Common words are automatically lowercased (except at the start):
- `The House Is Green` → `The House is Green`
- `When The User Is Ready` → `when the User is Ready`

Common words include: `the`, `a`, `an`, `and`, `or`, `is`, `are`, `was`, `were`, `has`, `have`, `in`, `on`, `at`, `to`, `of`, `by`, `with`, `from`, `as`, etc.

### 4. Article Selection

The correct article (a/an) is automatically chosen:
- `TestApple` → `an Apple`
- `TestBanana` → `a Banana`

> Prefer explicit control? Use the decorators (`describe`, `with_`, `without`, `when`, `it`) re-exported by `pytest_pyspec`. They override whatever automatic transformation would have done.

## Nesting Contexts

You can nest contexts to create complex hierarchies:

```python
class DescribeUserAuthentication:
    class WithValidCredentials:
        class WhenTheTwoFactorCodeIsCorrect:
            def it_logs_in_successfully(self):
                assert True
```

Output:
```
a User Authentication
  with Valid Credentials
    when the Two Factor Code is Correct
      ✓ logs in successfully
```

## Next Steps

- [Using Docstrings](docstrings.md) - Override automatic naming
- [Examples](examples.md) - See complete examples
