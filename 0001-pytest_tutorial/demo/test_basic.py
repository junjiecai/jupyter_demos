import pytest


def func(s, n):
    if not isinstance(s, str):
        raise TypeError('s should be string!')

    return s * n


def test_value_demo():
    assert func('ab', 3) == 'ababab'


def test_exception_demo():
    with pytest.raises(TypeError) as error_info:
        func(1, 3)

    assert 's should be string!' == str(error_info.value)
