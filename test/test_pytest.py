import pytest
import re


pytest_plugins = ["pytester"]


class TestFunction:

    def test_use_docstring(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_a():
                ''' it do something '''
                assert 1 == 1
        """)

        result = pytester.runpytest()
        output = '\n'.join(result.outlines)
        assert re.search(r'✓ it do something', output)

    def test_use_test_name(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)

        result = pytester.runpytest()
        output = '\n'.join(result.outlines)
        assert re.search(r'✓ it do something', output)
    
    def test_use_the_prefix_test(self, pytester: pytest.Pytester):
        assert 1 == 1
        return
    
    def it_use_the_prefix_it(self, pytester: pytest.Pytester):
        assert 1 == 1
        return
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)

        result = pytester.runpytest()
        output = '\n'.join(result.outlines)
        assert re.search(r'✓ it do something', output)


    class TestContext:
        def test_function(self):
            assert True
    

class TestCase:
    def test_case(self):
        assert True