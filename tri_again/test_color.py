import pytest
from ._color import normalize_color


def test_normalize_color():
    assert normalize_color("yellow") == (1, 1, 0)
    assert normalize_color((1, 0, 1)) == (1, 0, 1)

    with pytest.raises(
        ValueError,
        match="When specified as a tuple, color should be three floats between 0 and 1",
    ):
        normalize_color((1, 0))
    with pytest.raises(
        ValueError,
        match="When specified as a tuple, color should be three floats between 0 and 1",
    ):
        normalize_color((1, 0, 2))
