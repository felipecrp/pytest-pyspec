import pytest
from textwrap import dedent


pytest_plugins = ['pytest_pyspec', 'pytester']


class TestTestOutput:
    def test_show_the_test_name(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_show_the_test_name.py 
            ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)
    
    def test_use_test_with_prefix_test(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def test_do_something():
                assert 1 == 1
        """)
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_test_with_prefix_test.py 
            ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)
    
    def test_use_test_with_prefix_it(self, pytester: pytest.Pytester):
        pytester.makepyfile("""
            def it_do_something():
                assert 1 == 1
        """)
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_test_with_prefix_it.py 
            ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    class WithDocstring:
        def test_use_the_docstring(self, pytester: pytest.Pytester):
            pytester.makepyfile("""
                def test_a():
                    ''' do something '''
                    assert 1 == 1
            """)
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            
            expected = dedent("""
                test_use_the_docstring.py 
                ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

    class WithMultilineDocstring:
        def test_use_the_first_line(self, pytester: pytest.Pytester):
            pytester.makepyfile("""
                def test_do_something():
                    '''
                    do something with more details
                    '''
                    assert 1 == 1
            """)
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            
            expected = dedent("""
                test_use_the_first_line.py 
                ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

        class WithEmptyFirstLine:
            def test_use_the_formatted_name(self, pytester: pytest.Pytester):
                pytester.makepyfile("""
                    def test_do_something():
                        '''
                        with more details
                        '''
                        assert 1 == 1
                """)
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                
                expected = dedent("""
                    test_use_the_formatted_name.py 
                    ✓ do something
                """).strip()
                
                assert expected in output
                result.assert_outcomes(passed=1)


class TestTestCaseOutput:
    def test_show_the_described_object_name(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class TestThing:
                def test_do_something(self):
                    assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_show_the_described_object_name.py 
            A Thing
              ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    def test_use_the_prefix_describe(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class DescribeThing:
                def test_do_something(self):
                    assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_the_prefix_describe.py 
            A Thing
              ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    class WithDocstring:
        def test_use_the_docstring(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                class TestA:
                    """ thing """
                    def test_do_something(self):
                        assert 1 == 1
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            
            expected = dedent("""
                test_use_the_docstring.py 
                A thing
                  ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

    class WithMultilineDocstring:
        def test_use_the_first_line(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                class TestThing:
                    """
                    with more details
                    """
                    def test_do_something(self):
                        assert 1 == 1
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            
            expected = dedent("""
                test_use_the_first_line.py 
                A Thing
                  ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

        class WithEmptyFirstLine:
            def test_use_the_formatted_name(self, pytester: pytest.Pytester):
                pytester.makepyfile('''
                    class TestThing:
                        """
                        
                        with more details
                        """
                        def test_do_something(self):
                            assert 1 == 1
                ''')
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                
                expected = dedent("""
                    test_use_the_formatted_name.py 
                    A Thing
                      ✓ do something
                """).strip()
                
                assert expected in output
                result.assert_outcomes(passed=1)


class TestTestContextOutput:
    def test_show_the_context_name(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class TestThing:
                class WithContext:
                    def test_do_something(self):
                        assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_show_the_context_name.py 
            A Thing
              with Context
                ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    def test_use_the_formatted_name(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class TestThing:
                class TestSomeContext:
                    def test_do_something(self):
                        assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_the_formatted_name.py 
            A Thing
              with Some Context
                ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    def test_use_the_prefix_with(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class TestThing:
                class WithContext:
                    def test_do_something(self):
                        assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_the_prefix_with.py 
            A Thing
              with Context
                ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    def test_use_the_prefix_without(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            class TestThing:
                class WithoutContext:
                    def test_do_something(self):
                        assert 1 == 1
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_use_the_prefix_without.py 
            A Thing
              without Context
                ✓ do something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)

    class WithDocstring:
        def test_use_the_docstring(self, pytester: pytest.Pytester):
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
            
            expected = dedent("""
                test_use_the_docstring.py 
                A thing
                  with context
                    ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

    class WithMultilineDocstring:
        def test_use_the_first_line(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                class TestA:
                    """ thing """
                    class WithB:
                        """ context
                        with context and more details
                        """
                        def test_do_something(self):
                            assert 1 == 1
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)
            
            expected = dedent("""
                test_use_the_first_line.py 
                A thing
                  with context
                    ✓ do something
            """).strip()
            
            assert expected in output
            result.assert_outcomes(passed=1)

        class WithEmptyFirstLine:
            def test_use_the_formatted_name(self, pytester: pytest.Pytester):
                pytester.makepyfile('''
                    class TestA:
                        """ thing """
                        class WithContext:
                            """
                            
                            with more details
                            """
                            def test_do_something(self):
                                assert 1 == 1
                ''')
                result = pytester.runpytest('--pyspec')
                output = '\n'.join(result.outlines)
                
                expected = dedent("""
                    test_use_the_formatted_name.py 
                    A thing
                      with Context
                        ✓ do something
                """).strip()
                
                assert expected in output
                result.assert_outcomes(passed=1)



class TestModuleOutput:
    def test_show_the_module_name(self, pytester: pytest.Pytester):
        pytester.makepyfile(test_example='''
            class TestExample:
                def test_something(self):
                    assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_example.py 
            An Example
              ✓ something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)
    
    def test_show_its_tests(self, pytester: pytest.Pytester):
        pytester.makepyfile(test_example='''
            class TestExample:
                def test_first(self):
                    assert True
                
                def test_second(self):
                    assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            test_example.py 
            An Example
              ✓ first
              ✓ second
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=2)


class TestPackageOutput:
    def test_show_the_package_name(self, pytester: pytest.Pytester):
        pytester.mkpydir("mypackage")
        pytester.makepyfile(**{
            "mypackage/test_example.py": '''
                class TestExample:
                    def test_something(self):
                        assert True
            '''
        })
        
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        expected = dedent("""
            mypackage/test_example.py 
            An Example
              ✓ something
        """).strip()
        
        assert expected in output
        result.assert_outcomes(passed=1)
    
    def test_show_its_modules(self, pytester: pytest.Pytester):
        pytester.mkpydir("mypackage")
        pytester.makepyfile(**{
            "mypackage/test_alpha.py": '''
                class TestAlpha:
                    def test_something(self):
                        assert True
            '''
        })
        pytester.makepyfile(**{
            "mypackage/test_beta.py": '''
                class TestBeta:
                    def test_something(self):
                        assert True
            '''
        })
        
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)
        
        # Check both modules are shown with their tests
        expected_alpha = dedent("""
            mypackage/test_alpha.py 
            An Alpha
              ✓ something
        """).strip()
        
        expected_beta = dedent("""
            mypackage/test_beta.py 
            A Beta
              ✓ something
        """).strip()
        
        assert expected_alpha in output
        assert expected_beta in output
        result.assert_outcomes(passed=2)
