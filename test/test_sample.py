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

        def test_it_has_second_floor(self):
            assert 1 == 1

        @pytest.mark.xfail
        def test_third_floor(self):
            "has third floor"
            assert 1 == 2
