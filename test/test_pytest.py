import pytest
import re


pytest_plugins = ['pytest_pyspec', 'pytester']


class DescribeFunction:
    def test_use_test_name(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        assert re.search(r'^✓ do something', output, re.MULTILINE)
        result.assert_outcomes(passed=1)
    
    def test_use_the_prefix_test(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        assert re.search(r'^✓ do something', output, re.MULTILINE)
        result.assert_outcomes(passed=1)
    
    # @pytest.mark.skip
    def test_use_the_prefix_it(self, pytester: pytest.Pytester):
        pytester.makepyfile(
            """
            def it_do_something():
                assert 1 == 1
            """
        )
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        assert re.search(r'^✓ do something', output, re.MULTILINE)
        result.assert_outcomes(passed=1)

    class WithDocstring:
        def test_use_docstring(self, pytester: pytest.Pytester):
            pytester.makepyfile("""
                def test_a():
                    ''' do something '''
                    assert 1 == 1
            """)
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            assert re.search(r'^✓ do something', output, re.MULTILINE)
            result.assert_outcomes(passed=1)

    class WithTestCase:
        def test_show_the_test_case(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                class TestThing:
                    def test_do_something(self):
                        assert 1 == 1
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            assert re.search(r'^A Thing', output, re.MULTILINE)
            assert re.search(r'^  ✓ do something', output, re.MULTILINE)
            result.assert_outcomes(passed=1)

        def test_use_the_prefix_describe(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                class DescribeThing:
                    def test_do_something(self):
                        assert 1 == 1
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            assert re.search(r'^A Thing', output, re.MULTILINE)
            assert re.search(r'^  ✓ do something', output, re.MULTILINE)
            result.assert_outcomes(passed=1)

        class WithDocstring:
            def test_show_the_test_case_docstring(self, pytester: pytest.Pytester):
                pytester.makepyfile('''
                    class TestA:
                        """ thing """
                        def test_do_something(self):
                            assert 1 == 1
                ''')
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                assert re.search(r'^a thing', output, re.MULTILINE)
                assert re.search(r'^  ✓ do something', output, re.MULTILINE)
                result.assert_outcomes(passed=1)
    
        class WithContext:
            # @pytest.mark.skip
            def test_show_the_context(self, pytester: pytest.Pytester):
                pytester.makepyfile('''
                    class TestThing:
                        class WithContext:
                            def test_do_something(self):
                                assert 1 == 1
                ''')
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                assert re.search(r'^A Thing', output, re.MULTILINE)
                assert re.search(r'^  with Context', output, re.MULTILINE)
                assert re.search(r'^    ✓ do something', output, re.MULTILINE)
                result.assert_outcomes(passed=1)

            # @pytest.mark.skip
            def test_handle_negative_context(self, pytester: pytest.Pytester):
                pytester.makepyfile('''
                    class TestThing:
                        class WithoutContext:
                            def test_do_something(self):
                                assert 1 == 1
                ''')
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                assert re.search(r'^A Thing', output, re.MULTILINE)
                assert re.search(r'^  without Context', output, re.MULTILINE)
                assert re.search(r'^    ✓ do something', output, re.MULTILINE)
                result.assert_outcomes(passed=1)
                
            class WithDocstring:
                def test_show_the_context_docstring(self, pytester: pytest.Pytester):
                    pytester.makepyfile('''
                        class TestA:
                            """ thing """
                            class TestB:
                                """ with context """
                                def test_do_something(self):
                                    assert 1 == 1
                    ''')
                    result = pytester.runpytest('--pyspec')
                    output = '\n'.join(result.outlines)
                    assert re.search(r'^a thing', output, re.MULTILINE)
                    assert re.search(r'^  with context', output, re.MULTILINE)
                    assert re.search(r'^    ✓ do something', output, re.MULTILINE)
                    result.assert_outcomes(passed=1)

                def test_show_the_negative_context_docstring(self, pytester: pytest.Pytester):
                    pytester.makepyfile('''
                        class TestA:
                            """ thing """
                            class TestB:
                                """ without context """
                                def test_do_something(self):
                                    assert 1 == 1
                    ''')
                    result = pytester.runpytest('--pyspec')
                    output = '\n'.join(result.outlines)
                    assert re.search(r'^a thing', output, re.MULTILINE)
                    assert re.search(r'^  without context', output, re.MULTILINE)
                    assert re.search(r'^    ✓ do something', output, re.MULTILINE)
                    result.assert_outcomes(passed=1)


