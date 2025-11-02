from dataclasses import dataclass
from datetime import date

@dataclass
class Booking:
    id: int
    room_id: int
    customer_name: str
    start_date: date
    end_date: date
