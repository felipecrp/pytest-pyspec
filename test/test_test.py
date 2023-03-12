import re

pytest_plugins = ["pytester"]

class Test:
    "A Test" 

    class with_docstring:
        "with docstring"

        def test_docstring(self, pytester):
            "shows the docstring"
            pytester.makepyfile("""
                def test_hello():
                    '''say hello'''
                    assert 1 == 1
            """)

            result = pytester.runpytest()
            output = '\n'.join(result.outlines)
            assert re.search(r'✓ Say hello', output)

    class with_multiline_docstring:
        "with multiline docstring"

        def test_docstring(self, pytester):
            "shows the first line of the docstring"
            pytester.makepyfile("""
                def test_hello():
                    '''say hello
                    hidden text'''
                    assert 1 == 1
            """)

            result = pytester.runpytest()
            output = '\n'.join(result.outlines)
            assert re.search(r'✓ Say hello', output)
            assert not re.search(r'hidden text', output)

class TestCase:
    "A test case"

    class with_docstring:
        "with docstring"

        def test_docstring(self, pytester):
            "shows the docstring"
            pytester.makepyfile("""
                class TestHello:
                    '''A hello'''
                    def test_hello(self):
                        '''say hello'''
                        assert 1 == 1
            """)

            result = pytester.runpytest()
            output = '\n'.join(result.outlines)
            assert re.search(r'A hello\n  ✓ Say hello', output)

    class with_multiline_docstring:
        "with multiline docstring"

        def test_docstring(self, pytester):
            "shows the first line of the docstring"
            pytester.makepyfile("""
                class TestHello:
                    '''A hello
                    hidden text'''
                    def test_hello(self):
                        '''say hello'''
                        assert 1 == 1
            """)

            result = pytester.runpytest()
            output = '\n'.join(result.outlines)
            assert re.search(r'A hello\n  ✓ Say hello', output)
            assert not re.search(r'hidden text', output)
