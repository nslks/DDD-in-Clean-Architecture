import pytest
from datetime import date
from src.controller.booking_controller import BookingController
from src.repository.booking_repository import BookingRepository

@pytest.fixture
def controller():
    repo = BookingRepository()
    return BookingController(repo)

def test_booking_too_long(controller):
    with pytest.raises(ValueError, match="Booking too long"):
        controller.create_booking(
            room_id=1,
            customer_name="Bob",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 20)
        )

def test_booking_overlap(controller):
    # erste Buchung erfolgreich
    controller.create_booking(
        room_id=1,
        customer_name="Alice",
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 5)
    )

    # zweite überlappt -> Fehler
    with pytest.raises(ValueError, match="Room not available"):
        controller.create_booking(
            room_id=1,
            customer_name="Bob",
            start_date=date(2025, 11, 3),
            end_date=date(2025, 11, 6)
        )
