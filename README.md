[![](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml/badge.svg)](https://github.com/felipecrp/pytest-pyspec/actions/workflows/pytest.yml)

The **pytest-pyspec** plugin provides semantics to the pytest output. It
transforms the pytest's output into a result similar to the RSpec.

The default pytest output is like the following:

```
test/test_pytest.py::TestFunction::test_use_test_name PASSED
test/test_pytest.py::TestFunction::test_use_the_prefix_test PASSED
test/test_pytest.py::TestFunction::test_use_the_prefix_it PASSED
test/test_pytest.py::TestFunction::WithDocstring::test_use_docstring PASSED
```
The **pytest-pyspec** transforms the output into the following:

```
A function
  ✓ use test name
  ✓ use the prefix test
  ✓ use the prefix it

A function
  with docstring
    ✓ use docstring
```

You just need to prefix your test case classes with:

- _describe / test_ to represent objects
- _with / without_ to represent context 

And prefix your tests with:

- _it / test_ to represent objects

The following is a sample test that generates the previous tests` output.

```python
class TestFunction:
    def test_use_test_name(self):
        assert 1 == 1
    
    def test_use_the_prefix_test(self):
        assert 1 == 1
    
    def test_use_the_prefix_it(self):
        assert 1 == 1

    class WithDocstring:
        def test_use_docstring(self):
            assert 1 == 1
```

Moreover, you can use a docstring to overwrite the test description. The
following tests have the same output as the previous tests:

```python
class TestA:
    """ Function """
    def test_1(self):
        """ use test name """
        assert 1 == 1
    
    def test_2(self):
        """ use the prefix test """
        assert 1 == 1
    
    def test_3(self):
        """ use the prefix it """
        assert 1 == 1

    class TestB:
        """ with docstring """
        def test_4(self):
            """ use docstring """
            assert 1 == 1
```

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
pip install pytest pytest-pyspec
pytest --pyspec
```
