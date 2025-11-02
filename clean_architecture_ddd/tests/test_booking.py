import pytest
from datetime import date
from src.domain.booking import Booking

def test_create_valid_booking():
    booking = Booking(
        booking_id=1,
        room_id=1,
        customer_name="Hans",
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 5)
    )
    assert booking.room_id == 1
    assert booking.start_date < booking.end_date

def test_booking_too_long():
    with pytest.raises(ValueError, match="cannot exceed 10 days"):
        Booking(
            booking_id=1,
            room_id=1,
            customer_name="Bob",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 20)
        )

def test_booking_overlap():
    b1 = Booking(
        booking_id=1,
        room_id=1,
        customer_name="Alice",
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 5)
    )
    b2 = Booking(
        booking_id=2,
        room_id=1,
        customer_name="Bob",
        start_date=date(2025, 11, 3),
        end_date=date(2025, 11, 6)
    )
    assert b1.overlaps(b2)
