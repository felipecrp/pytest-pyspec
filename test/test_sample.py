
import pytest

class TestHouse:
    "a House"
    
    def test_has_door(self):
        "has door"
        assert 1 == 1
        
    class TestTwoFloors:
        "with two floors"

        def test_has_stairs(self):
            "has stairs"
            assert 1 == 1

        def test_has_second_floor(self):
            "has second floor"
            assert 1 == 1
