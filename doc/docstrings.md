# Using Docstrings

While pytest-pyspec automatically generates readable descriptions from class and function names, you can use docstrings to provide completely custom descriptions.

## Basic Docstring Usage

### Overriding Class Descriptions

```python
class TestPaymentGateway:
    """payment processor"""
    
    def test_processes_credit_cards(self):
        assert True
```

Output:
```
a payment processor
  ✓ processes credit cards
```

### Overriding Test Descriptions

```python
class DescribeUser:
    def test_validation(self):
        """validates email format correctly"""
        assert True
```

Output:
```
a User
  ✓ validates email format correctly
```

### Overriding Context Descriptions

```python
class TestShoppingCart:
    class WithItems:
        """with 3 items in the cart"""
        
        def test_total(self):
            assert True
```

Output:
```
a Shopping Cart
  with 3 items in the cart
    ✓ total
```

## Multiline Docstrings

When using multiline docstrings, **pytest-pyspec** only uses the **very first line as-is**.
If that line is empty (a common pattern when using triple-quoted strings), the docstring
is ignored and the identifier-derived description is used instead. Keep the first line
non-empty to ensure the docstring takes effect.

```python
class DescribeCalculator:
    """
    advanced scientific calculator
    with support for complex operations
    """
    
    def test_addition(self):
        """
        adds two numbers correctly
        this is a very important test
        """
        assert True
```

Output:
```
an advanced scientific calculator
  ✓ adds two numbers correctly
```

## Docstring Best Practices

### 1. Keep It Concise

Docstrings for test descriptions should be brief and to the point.

❌ **Too Verbose:**
```python
def test_user_login(self):
    """
    This test verifies that when a user provides valid credentials,
    they are able to successfully log into the system and receive
    an authentication token that can be used for subsequent requests.
    """
    assert True
```

✅ **Better:**
```python
def test_user_login(self):
    """logs in with valid credentials"""
    assert True
```

### 2. Use Lowercase (pytest-pyspec handles capitalization)

```python
class TestAPI:
    """REST API endpoint"""
    
    def test_authentication(self):
        """requires authentication token"""
        assert True
```

Output:
```
a REST API endpoint
  ✓ requires authentication token
```

### 3. Match the Prefix Style

For contexts, don't repeat the prefix in the docstring:

❌ **Redundant:**
```python
class WithPermissions:
    """with admin permissions"""
    pass
```

✅ **Better:**
```python
class WithPermissions:
    """admin permissions"""
    pass
```

Both produce: `with admin permissions`

### 4. Combine Docstrings with Naming

You can mix docstrings and automatic naming:

```python
class DescribeUserAuthentication:
    """user login system"""
    
    class WhenThePasswordIsWrong:
        def test_rejects_login(self):
            assert True
        
        def test_increments_failed_attempts(self):
            """tracks failed login attempts"""
            assert True
```

Output:
```
a user login system
  when the Password is Wrong
    ✓ rejects login
    ✓ tracks failed login attempts
```

## When to Use Docstrings

### Use Docstrings When:

1. **The automatic name is awkward**
   ```python
   class TestHTTPSConnectionWithSSLv3:
       """HTTPS connection using SSL v3"""
   ```

2. **You need special formatting or numbers**
   ```python
   def test_http_status():
       """returns 404 status code"""
   ```

3. **The domain language differs from code**
   ```python
   class TestUserAuthenticationService:
       """login functionality"""
   ```

### Use Automatic Naming When:

1. **Names are already clear**
   ```python
   class DescribeShoppingCart:  # "a Shopping Cart" is perfect
   ```

2. **Standard patterns work well**
   ```python
   def test_adds_items():  # "adds items" is clear
   ```

3. **Consistency is important**
   - Automatic naming ensures consistent style across tests

## Docstring Filtering

pytest-pyspec automatically filters out common filler text from docstrings:

```python
def test_example():
    """
    validates user input
    with more details
    """
    assert True
```

The phrase "with more details" is filtered out, resulting in:
```
✓ validates user input
```

## Advanced: Mixing Styles

You can strategically mix docstrings and automatic naming:

```python
class DescribePaymentProcessing:
    """payment gateway integration"""
    
    class WhenTheCardIsValid:
        # Uses automatic naming
        
        def test_charges_successfully(self):
            # Uses automatic naming
            assert True
        
        def test_response_time(self):
            """completes in under 2 seconds"""
            assert True
    
    class WhenTheCardExpires:
        """when the credit card has expired"""
        
        def test_reject(self):
            """declines the transaction"""
            assert True
```

Output:
```
a payment gateway integration
  when the Card is Valid
    ✓ charges successfully
    ✓ completes in under 2 seconds

  when the credit card has expired
    ✓ declines the transaction
```

## Next Steps

- [Advanced Features](advanced-features.md) - Explore more capabilities
- [Examples](examples.md) - See complete test suites
