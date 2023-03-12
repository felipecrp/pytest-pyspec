[![](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml/badge.svg)](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml)

The **pytest-pyspec** plugin transforms the pytest output into a result similar to the RSpec.

Just nest your tests using classes and include _docstring_ for each class and test. You can create any nested levels.

The following test sample:

```python
import pytest

class TestHouse:
    "a House"
    
    def test_door(self):
        "has door"
        assert 1 == 1
        
    class TestTwoFloors:
        """with two floors
        
        A house with two floor has stairs
        """
        def test_stairs(self):
            "has stairs"
            assert 1 == 1

        def test_second_floor(self):
            "has second floor"
            assert 1 == 1

        def test_third_floor(self):
            "has third floor"
            assert 1 == 2
```

Generates the following output:

```
test/test_sample.py 

A house
  ✓ Has door

A house
  With two floors
    ✓ Has stairs
    ✓ Has second floor
    ✗ Has third floor
```

## Installing and running **pySpec**

```bash
pip install pytest-pyspec
pytest --pyspec
```
