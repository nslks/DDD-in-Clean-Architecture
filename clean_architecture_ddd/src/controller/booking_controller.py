from src.domain.booking import Booking

class BookingController:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, room_id, customer_name, start_date, end_date):
        new_booking = Booking(
            room_id=room_id,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date
        )

        for existing in self.repo.all():
            if new_booking.overlaps(existing):
                raise ValueError("Room not available for given dates")

        return self.repo.save(new_booking)
    
    def get_all_bookings(self):
        return self.repo.all()
