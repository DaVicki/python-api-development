import pytest 

@pytest.fixture
def ba():
    return 1

@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (3, 4, 7)])
def test_sum(a: int, b: int, expected: int):
    c = a + b
    assert c == expected

def test_fixture(ba):
    assert ba == 1

def test_expection(ba):
    with pytest.raises(ZeroDivisionError):
        c = ba / 0