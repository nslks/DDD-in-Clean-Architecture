from src.model.booking import Booking

class BookingController:
    def __init__(self, repo):
        self.repo = repo

    def _booking_lasts_longer_than_max_days(self, start_date, end_date):
        max_allowed_day = 10

        days = (end_date - start_date).days
        return days > max_allowed_day
    
    def _room_not_available(self, existing, room_id, start_date, end_date):
        same_room = existing.room_id == room_id
        overlapping = not (end_date <= existing.start_date or start_date >= existing.end_date)
        return same_room and overlapping

    def create_booking(self, room_id, customer_name, start_date, end_date):
        
        # erste fachliche Regel
        if self._booking_lasts_longer_than_max_days(start_date, end_date):
            raise ValueError(f"Booking too long")
        
        # zweite fachliche Regel: Überschneidungen prüfen (innerhalb Use Case)
        for existing in self.repo.all():
            if self._room_not_available(existing, room_id, start_date, end_date):
                raise ValueError("Room not available for given dates")
            
        booking = Booking(
            id=0,
            room_id=room_id,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date
        )

        return self.repo.save(booking)
    
    def get_all_bookings(self):
        return self.repo.all()
