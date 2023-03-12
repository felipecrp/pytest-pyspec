pytest_plugins = ["pytester"]

class Test:
    "A Test" 

    class with_docstring:

        def test_docstring(self, pytester):
            pytester.makepyfile("""
                def test_hello():
                    assert 1 == 1
            """)

            result = pytester.runpytest()
            assert 1 == 1

def test_hello():
    assert 1 == 1
