from datetime import time

import pytest

from src.utils.global_utils import subtract_minutes


@pytest.mark.parametrize(
    "orig_time, minutes, expected_time",
    [
        (time(15, 50), 15, time(15, 35)),
        (time(0, 50), 50, time(0, 0)),
        (time(0, 0), 1, time(23, 59)),
    ],
)
def test_subtract_minutes(orig_time: time, minutes: int, expected_time: time) -> None:
    assert subtract_minutes(orig_time, minutes) == expected_time
