import time
from contextlib import nullcontext as does_not_raise_error

import pytest
from fastapi import HTTPException
from freezegun import freeze_time

from core import validate_car_uid, validate_reservation_time


@freeze_time("2023-06-25 20:00:00")
@pytest.mark.parametrize(
    "now_offset_start, now_offset_end, expected",
    [
        (0, 60, does_not_raise_error()),
        (60, 600, does_not_raise_error()),
        (0, -60, pytest.raises(HTTPException)),  # end is sooner than start
        (24 * 60 * 60 + 60,24 * 60 * 60 + 120,pytest.raises(HTTPException)),  # reservations start is more than 24 hours from now
        (0, 0, pytest.raises(HTTPException)),  # start time is same as end time
        (-60, 0, pytest.raises(HTTPException)),  # start time in the past
        (0, 3 * 60 * 60, pytest.raises(HTTPException)),  # reservation longer than 2 hours
    ],
)
def test_validate_reservation_time(now_offset_start, now_offset_end, expected):
    now_timestamp = int(time.time())
    with expected:
        validate_reservation_time(now_timestamp + now_offset_start, now_timestamp + now_offset_end)


@pytest.mark.parametrize(
    "car_uid, expected",
    [
        ("C1", does_not_raise_error()),
        ("C123456789", does_not_raise_error()),
        ("C1234567890", pytest.raises(HTTPException)),  # number too long
        ("c123", pytest.raises(HTTPException)),
        ("A123456789", pytest.raises(HTTPException)),
        ("C", pytest.raises(HTTPException)),
        ("C123a", pytest.raises(HTTPException)),
        ("123", pytest.raises(HTTPException)),
        ("abcd", pytest.raises(HTTPException)),
    ],
)
def test_validate_car_uid(car_uid, expected):
    with expected:
        validate_car_uid(car_uid)
