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
            assert 1 == 2

        def test_second_floor(self):
            "has second floor"
            assert 1 == 1
