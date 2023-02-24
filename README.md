
The **pySpec** plugin transforms the pytest output into RSpec.

Just nest your tests using classes and include _docstring_ for each class and test. You can create any nested levels.

The following test sample:

```python
import pytest

class TestHouse:
    "a House"
    
    def test_door(self):
        "has a door"
        assert 1 == 1
        
    class TestTwoFloors:
        "with two floors"

        def test_stairs(self):
            "has stairs"
            assert 1 == 1

        def test_second_floor(self):
            "has second floor"
            assert 1 == 1
```

Generates the following output:

```
test/test_sample.py 
  A house
    Has a door                                                       .
  A house
    With two floors
      Has stairs                                                     .
      Has second floor                                               .      [100%]
```

## Installing and running **pySpec**

```bash
pip install pytest-pyspec
pytest --pyspec
```