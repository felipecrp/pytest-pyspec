# Examples

This page contains complete, real-world examples demonstrating pytest-pyspec's features.

## Example 1: E-commerce Shopping Cart

```python
import pytest

class DescribeShoppingCart:
    """shopping cart system"""
    
    def test_starts_empty(self):
        cart = ShoppingCart()
        assert cart.item_count() == 0
    
    def test_calculates_empty_total(self):
        cart = ShoppingCart()
        assert cart.total() == 0
    
    class WhenItemsAreAdded:
        def test_increases_item_count(self):
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            assert cart.item_count() == 1
        
        def test_updates_total_price(self):
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            cart.add_item(Product("Pen", 2.50))
            assert cart.total() == 12.50
    
    class WhenItemsAreRemoved:
        def test_decreases_item_count(self):
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            cart.remove_item("Book")
            assert cart.item_count() == 0
        
        def test_updates_total_price(self):
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            cart.add_item(Product("Pen", 2.50))
            cart.remove_item("Pen")
            assert cart.total() == 10.00
    
    class WithDiscountCode:
        def test_applies_percentage_discount(self):
            """applies 20% discount with valid code"""
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            cart.apply_discount("SAVE20")
            assert cart.total() == 8.00
        
        def test_rejects_invalid_code(self):
            """ignores invalid discount codes"""
            cart = ShoppingCart()
            cart.add_item(Product("Book", 10.00))
            cart.apply_discount("INVALID")
            assert cart.total() == 10.00
```

**Output:**
```
a shopping cart system
  ✓ starts empty
  ✓ calculates empty total

  when Items are Added
    ✓ increases item count
    ✓ updates total price

  when Items are Removed
    ✓ decreases item count
    ✓ updates total price

  with Discount Code
    ✓ applies 20% discount with valid code
    ✓ ignores invalid discount codes
```

## Example 2: User Authentication

```python
import pytest

class DescribeUserAuthentication:
    class WithValidCredentials:
        @pytest.fixture
        def user_data(self):
            return {"email": "user@example.com", "password": "SecurePass123"}
        
        def test_authenticates_successfully(self, user_data):
            result = authenticate(user_data["email"], user_data["password"])
            assert result.success is True
        
        def test_returns_auth_token(self, user_data):
            result = authenticate(user_data["email"], user_data["password"])
            assert result.token is not None
        
        def test_sets_login_timestamp(self, user_data):
            result = authenticate(user_data["email"], user_data["password"])
            assert result.logged_in_at is not None
    
    class WithInvalidCredentials:
        def test_rejects_wrong_password(self):
            result = authenticate("user@example.com", "WrongPassword")
            assert result.success is False
        
        def test_does_not_return_token(self):
            result = authenticate("user@example.com", "WrongPassword")
            assert result.token is None
        
        def test_increments_failed_attempts(self):
            """tracks failed login attempts for security"""
            user = User.find_by_email("user@example.com")
            authenticate("user@example.com", "WrongPassword")
            assert user.failed_login_attempts == 1
    
    class WhenTheAccountIsLocked:
        def test_prevents_login_attempts(self):
            """blocks login even with correct credentials"""
            user = User.find_by_email("locked@example.com")
            user.lock_account()
            result = authenticate("locked@example.com", "CorrectPassword")
            assert result.success is False
            assert result.error == "Account is locked"
    
    class WhenTheTwoFactorCodeIsRequired:
        def test_prompts_for_verification_code(self):
            result = authenticate("2fa@example.com", "CorrectPassword")
            assert result.requires_2fa is True
        
        class WithCorrectCode:
            def test_completes_authentication(self):
                partial_auth = authenticate("2fa@example.com", "CorrectPassword")
                result = verify_2fa(partial_auth.session_id, "123456")
                assert result.success is True
        
        class WithIncorrectCode:
            def test_rejects_authentication(self):
                partial_auth = authenticate("2fa@example.com", "CorrectPassword")
                result = verify_2fa(partial_auth.session_id, "wrong")
                assert result.success is False
```

**Output:**
```
a User Authentication
  with Valid Credentials
    ✓ authenticates successfully
    ✓ returns auth token
    ✓ sets login timestamp

  with Invalid Credentials
    ✓ rejects wrong password
    ✓ does not return token
    ✓ tracks failed login attempts for security

  when the Account is Locked
    ✓ blocks login even with correct credentials

  when the Two Factor Code is Required
    ✓ prompts for verification code

    with Correct Code
      ✓ completes authentication

    with Incorrect Code
      ✓ rejects authentication
```

## Example 3: REST API

```python
import pytest

class DescribeProductsAPI:
    """Products REST API endpoint"""
    
    class WithAuthentication:
        def test_lists_all_products(self, auth_client):
            """GET /api/products returns product list"""
            response = auth_client.get("/api/products")
            assert response.status_code == 200
            assert len(response.json()["products"]) > 0
        
        def test_creates_new_product(self, auth_client):
            """POST /api/products creates a product"""
            data = {"name": "Widget", "price": 9.99}
            response = auth_client.post("/api/products", json=data)
            assert response.status_code == 201
            assert response.json()["name"] == "Widget"
        
        def test_updates_existing_product(self, auth_client):
            """PUT /api/products/:id updates the product"""
            data = {"name": "Updated Widget", "price": 12.99}
            response = auth_client.put("/api/products/1", json=data)
            assert response.status_code == 200
            assert response.json()["price"] == 12.99
        
        def test_deletes_product(self, auth_client):
            """DELETE /api/products/:id removes the product"""
            response = auth_client.delete("/api/products/1")
            assert response.status_code == 204
    
    class WithoutAuthentication:
        def test_returns_401_unauthorized(self, client):
            """requires authentication for all operations"""
            response = client.get("/api/products")
            assert response.status_code == 401
    
    class WhenTheProductDoesNotExist:
        def test_returns_404_not_found(self, auth_client):
            """GET /api/products/999 returns 404"""
            response = auth_client.get("/api/products/999")
            assert response.status_code == 404
    
    class WithInvalidData:
        @pytest.mark.parametrize("invalid_data,expected_error", [
            ({"name": ""}, "Name is required"),
            ({"price": -5}, "Price must be positive"),
            ({"price": "not-a-number"}, "Price must be numeric"),
        ])
        def test_rejects_invalid_input(self, auth_client, invalid_data, expected_error):
            """validates input and returns helpful errors"""
            response = auth_client.post("/api/products", json=invalid_data)
            assert response.status_code == 400
            assert expected_error in response.json()["error"]
```

**Output:**
```
a Products REST API endpoint
  with Authentication
    ✓ GET /api/products returns product list
    ✓ POST /api/products creates a product
    ✓ PUT /api/products/:id updates the product
    ✓ DELETE /api/products/:id removes the product

  without Authentication
    ✓ requires authentication for all operations

  when the Product Does not Exist
    ✓ GET /api/products/999 returns 404

  with Invalid Data
    ✓ validates input and returns helpful errors[invalid_data0-Name is required]
    ✓ validates input and returns helpful errors[invalid_data1-Price must be positive]
    ✓ validates input and returns helpful errors[invalid_data2-Price must be numeric]
```

## Example 4: Database Operations

```python
import pytest

class DescribeDatabaseConnection:
    """database connection manager"""
    
    @pytest.fixture
    def db(self):
        connection = Database.connect("test.db")
        yield connection
        connection.close()
    
    class WhenTheConnectionIsActive:
        def test_executes_queries(self, db):
            result = db.query("SELECT 1")
            assert result is not None
        
        def test_supports_transactions(self, db):
            """begins and commits transactions"""
            db.begin_transaction()
            db.execute("INSERT INTO users (name) VALUES ('Test')")
            db.commit()
            assert db.query("SELECT COUNT(*) FROM users")[0][0] == 1
    
    class WhenTheConnectionIsClosed:
        def test_raises_error_on_query(self, db):
            db.close()
            with pytest.raises(ConnectionError):
                db.query("SELECT 1")
    
    class WithInvalidCredentials:
        def test_fails_to_connect(self):
            """raises authentication error"""
            with pytest.raises(AuthenticationError):
                Database.connect("test.db", password="wrong")
```

**Output:**
```
a database connection manager
  when the Connection is Active
    ✓ executes queries
    ✓ begins and commits transactions

  when the Connection is Closed
    ✓ raises error on query

  with Invalid Credentials
    ✓ raises authentication error
```

## Example 5: File Processing

```python
import pytest
from pathlib import Path

class DescribeCSVProcessor:
    """CSV file processor"""
    
    @pytest.fixture
    def sample_csv(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,25")
        return csv_file
    
    def test_reads_csv_file(self, sample_csv):
        processor = CSVProcessor(sample_csv)
        data = processor.read()
        assert len(data) == 2
    
    def test_parses_headers(self, sample_csv):
        processor = CSVProcessor(sample_csv)
        assert processor.headers == ["name", "age"]
    
    class WhenTheFileIsEmpty:
        @pytest.fixture
        def empty_csv(self, tmp_path):
            csv_file = tmp_path / "empty.csv"
            csv_file.write_text("")
            return csv_file
        
        def test_returns_empty_list(self, empty_csv):
            processor = CSVProcessor(empty_csv)
            assert processor.read() == []
    
    class WhenTheFileHasMalformedData:
        @pytest.fixture
        def malformed_csv(self, tmp_path):
            csv_file = tmp_path / "bad.csv"
            csv_file.write_text("name,age\nAlice,30,extra\nBob")
            return csv_file
        
        def test_raises_parse_error(self, malformed_csv):
            processor = CSVProcessor(malformed_csv)
            with pytest.raises(ParseError):
                processor.read()
    
    class WithCustomDelimiter:
        @pytest.fixture
        def tsv_file(self, tmp_path):
            tsv = tmp_path / "data.tsv"
            tsv.write_text("name\tage\nAlice\t30")
            return tsv
        
        def test_parses_tab_delimited_files(self, tsv_file):
            """handles TSV files with custom delimiter"""
            processor = CSVProcessor(tsv_file, delimiter='\t')
            data = processor.read()
            assert len(data) == 1
            assert data[0]["name"] == "Alice"
```

**Output:**
```
a CSV file processor
  ✓ reads csv file
  ✓ parses headers

  when the File is Empty
    ✓ returns empty list

  when the File Has Malformed Data
    ✓ raises parse error

  with Custom Delimiter
    ✓ handles TSV files with custom delimiter
```

## Next Steps

- [Configuration](configuration.md) - Learn about configuration options
- [GitHub Repository](https://github.com/felipecrp/pytest-pyspec) - Contribute or report issues
