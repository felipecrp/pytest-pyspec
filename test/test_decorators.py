import pytest
from textwrap import dedent


pytest_plugins = ['pytest_pyspec', 'pytester']


class DescribeDecorator:

    def test_overrides_object_description(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            import pytest_pyspec as spec

            @spec.describe("Electric Car")
            class DescribeCombustionThing:
                def test_default_behavior(self):
                    assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)

        expected = dedent("""
            test_overrides_object_description.py 
            an Electric Car
              ✓ default behavior
        """).strip()

        assert expected in output
        result.assert_outcomes(passed=1)

    def test_overrides_test_description(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            import pytest_pyspec as spec

            @spec.describe("Widget")
            class DescribeWidget:
                @spec.it("spins rapidly")
                def test_slow_rotation(self):
                    assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)

        expected = dedent("""
            test_overrides_test_description.py 
            a Widget
              ✓ spins rapidly
        """).strip()

        assert expected in output
        result.assert_outcomes(passed=1)

    def test_overrides_context_with(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            import pytest_pyspec as spec

            @spec.describe("Device")
            class DescribeDevice:
                @spec.with_("charged battery")
                class WithDefaultContextName:
                    def test_runs_forever(self):
                        assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)

        expected = dedent("""
            test_overrides_context_with.py 
            a Device
              with charged battery
                ✓ runs forever
        """).strip()

        assert expected in output
        result.assert_outcomes(passed=1)

    def test_overrides_context_without_description(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            import pytest_pyspec as spec

            @spec.describe("Robot")
            class DescribeRobot:
                @spec.without("power")
                class WithoutEnergySupply:
                    def test_enters_sleep_mode(self):
                        assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)

        expected = dedent("""
            test_overrides_context_without_description.py 
            a Robot
              without power
                ✓ enters sleep mode
        """).strip()

        assert expected in output
        result.assert_outcomes(passed=1)

    def test_overrides_context_when_description(self, pytester: pytest.Pytester):
        pytester.makepyfile('''
            import pytest_pyspec as spec

            @spec.describe("Server")
            class DescribeServer:
                @spec.when("under heavy load")
                class WhenIdleByDefault:
                    def test_scales_up(self):
                        assert True
        ''')
        result = pytester.runpytest('--pyspec')
        output = '\n'.join(result.outlines)

        expected = dedent("""
            test_overrides_context_when_description.py 
            a Server
              when under heavy load
                ✓ scales up
        """).strip()

        assert expected in output
        result.assert_outcomes(passed=1)

    class WithDocstring:
        def test_overrides_object_description(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                import pytest_pyspec as spec

                @spec.describe("Electric Car")
                class DescribeCombustionThing:
                    """combustion vehicle"""
                    def test_default_behavior(self):
                        assert True
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)

            expected = dedent("""
                test_overrides_object_description.py 
                an Electric Car
                  ✓ default behavior
            """).strip()

            assert expected in output
            result.assert_outcomes(passed=1)

        def test_overrides_test_description(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                import pytest_pyspec as spec

                @spec.describe("Widget")
                class DescribeWidget:
                    @spec.it("spins rapidly")
                    def test_slow_rotation(self):
                        """rotates slowly"""
                        assert True
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)

            expected = dedent("""
                test_overrides_test_description.py 
                a Widget
                  ✓ spins rapidly
            """).strip()

            assert expected in output
            result.assert_outcomes(passed=1)

        def test_overrides_context_with(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                import pytest_pyspec as spec

                @spec.describe("Device")
                class DescribeDevice:
                    @spec.with_("charged battery")
                    class WithDefaultContextName:
                        """context docstring should not show"""
                        def test_runs_forever(self):
                            assert True
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)

            expected = dedent("""
                test_overrides_context_with.py 
                a Device
                  with charged battery
                    ✓ runs forever
            """).strip()

            assert expected in output
            result.assert_outcomes(passed=1)

        def test_overrides_context_without_description(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                import pytest_pyspec as spec

                @spec.describe("Robot")
                class DescribeRobot:
                    @spec.without("power")
                    class WithoutEnergySupply:
                        """docstring for without context"""
                        def test_enters_sleep_mode(self):
                            assert True
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)

            expected = dedent("""
                test_overrides_context_without_description.py 
                a Robot
                  without power
                    ✓ enters sleep mode
            """).strip()

            assert expected in output
            result.assert_outcomes(passed=1)

        def test_overrides_context_when_description(self, pytester: pytest.Pytester):
            pytester.makepyfile('''
                import pytest_pyspec as spec

                @spec.describe("Server")
                class DescribeServer:
                    @spec.when("under heavy load")
                    class WhenIdleByDefault:
                        """docstring for when context"""
                        def test_scales_up(self):
                            assert True
            ''')
            result = pytester.runpytest('--pyspec')
            output = '\n'.join(result.outlines)

            expected = dedent("""
                test_overrides_context_when_description.py 
                a Server
                  when under heavy load
                    ✓ scales up
            """).strip()

            assert expected in output
            result.assert_outcomes(passed=1)
