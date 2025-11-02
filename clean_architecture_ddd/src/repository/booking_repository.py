from typing import List
from src.domain.booking import Booking

class BookingRepository:
    def __init__(self):
        self._bookings: List[Booking] = []
        self._next_id = 1

    def save(self, booking: Booking) -> Booking:
        booking.id = self._next_id
        self._next_id += 1
        self._bookings.append(booking)
        return booking

    def all(self) -> list[Booking]:
        return list(self._bookings)
