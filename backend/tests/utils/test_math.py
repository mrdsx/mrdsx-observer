from src.utils.math import truncate


def test_truncate():
    assert truncate(1.234, 0) == 1
    assert truncate(1.934, 0) == 1
    assert truncate(2.718, 1) == 2.7
    assert truncate(3.14159, 1) == 3.1
    assert truncate(3.915, 2) == 3.91
    assert truncate(314.5101, 2) == 314.51
