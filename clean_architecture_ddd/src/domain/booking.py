from datetime import date

MAX_BOOKING_DAYS = 10 # jaja geht besser ich weis

class Booking:
    def __init__(self, booking_id, room_id, customer_name, start_date, end_date):
        if start_date >= end_date:
            raise ValueError("end_date must be after start_date")

        duration = (end_date - start_date).days
        if duration > MAX_BOOKING_DAYS:
            raise ValueError(f"Booking cannot exceed {MAX_BOOKING_DAYS} days")

        self.id = booking_id
        self.room_id = room_id
        self.customer_name = customer_name
        self.start_date = start_date
        self.end_date = end_date
    
    
    def overlaps(self, other):
        return self.room_id == other.room_id and not (
            self.end_date <= other.start_date or self.start_date >= other.end_date
        )

