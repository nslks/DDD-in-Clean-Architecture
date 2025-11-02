from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
from src.controller.booking_controller import BookingController
from src.repository.booking_repository import BookingRepository

app = FastAPI(title="Booking System - Clean Architecture")

repo = BookingRepository()
controller = BookingController(repo)

class BookingRequest(BaseModel):
    room_id: int
    customer_name: str
    start_date: date
    end_date: date

@app.post("/bookings")
def create_booking(request: BookingRequest):
    try:
        return controller.create_booking(
            request.room_id,
            request.customer_name,
            request.start_date,
            request.end_date
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bookings")
def list_bookings():
    return controller.get_all_bookings()
